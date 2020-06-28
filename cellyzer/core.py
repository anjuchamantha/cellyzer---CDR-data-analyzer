"""
Main classes are modeled here

"""

from operator import itemgetter

from . import tools
from . import visualization
from . import utils

import datetime


# Classes for Records
class Record:
    pass


class CallRecord(Record):

    def __init__(self, user, other_user, direction, duration, timestamp, cell_id, cost, index=""):
        self.index = index
        self.user = user
        self.other_user = other_user
        self.direction = direction
        self.duration = duration
        self.timestamp = timestamp
        self.cell_id = cell_id
        self.cost = cost

    def get_user(self):
        return self.user

    def get_other_user(self):
        return self.other_user

    def get_direction(self):
        return self.direction

    def get_duration(self):
        return self.duration

    def get_timestamp(self):
        return self.timestamp

    def get_cell_id(self):
        return self.cell_id

    def get_cost(self):
        return self.cost


class MessageRecord(Record):

    def __init__(self, user, other_user, direction, length, timestamp):
        self._user = user
        self._other_user = other_user
        self._direction = direction
        self._length = length
        self._timestamp = timestamp

    def get_user(self):
        return self._user

    def get_other_user(self):
        return self._other_user

    def get_direction(self):
        return self._direction

    def get_duration(self):
        return self._length

    def get_timestamp(self):
        return self._timestamp


class CellRecord(Record):
    def __init__(self, cell_id, latitude, longitude):
        self._cell_id = cell_id
        self._latitude = latitude
        self._longitude = longitude

    def get_cell_id(self):
        return self._cell_id

    def get_latitude(self):
        return self._latitude

    def get_longitude(self):
        return self._longitude


# classes for DataSet
class DataSet:
    def __init__(self, records=None, fieldnames=None):
        self._fieldnames = fieldnames
        if records is None:
            self._records = []
        else:
            self._records = records

    def add_records(self, data):
        self._records.append(data)

    def get_records(self):
        return self._records

    def get_fieldnames(self):
        return self._fieldnames

    def to_dict(self):
        records_list = []
        for record in self.get_records():
            records_list.append(vars(record))
        return records_list


class CallMessageDataSet(DataSet):

    def get_records(self, user1=None, user2=None):
        """
        Get records of a given user or records between given 2 users

        :param user1: string or None
                contact number of user1

        :param user2: string or None
                contact number of user2

        :return: record(s) : list of records
        """
        all_records = super().get_records()
        records = []
        if (user1 is None) and (user2 is None):
            # calls the function of Dataset class
            # return all the records : List of Record objects
            return all_records
        elif type(user1) != str and type(user1) != int and user1 is not None:
            raise TypeError
        elif type(user2) != str and type(user2) != int and user2 is not None:
            raise TypeError
        for record in all_records:
            user = record.get_user()
            other_user = record.get_other_user()
            if (user1 is not None) and (user2 is None):
                # returns a list of Record objects where the given user is involved
                if str(user1) == user or str(user1) == other_user:
                    records.append(record)
            if (user1 is not None) and (user2 is not None):
                # returns a list of Record objects where the given 2 users are involved
                if (str(user1) == user and str(user2) == other_user) or (
                        str(user1) == other_user and str(user2) == user):
                    records.append(record)
        return records

    def get_all_users(self):
        """
        get all the different users in the CallDataSet

        :return: all_users : list
        """
        all_users = []
        for record in self.get_records():
            user = record.get_user()
            other_user = record.get_other_user()
            if user not in all_users:
                all_users.append(user)
            if other_user not in all_users:
                all_users.append(other_user)
        return all_users

    def get_connected_users(self, user):
        """
        get a list of users that are connected to a given user

        :param user: string

        :return: connected_users : list
        """
        if type(user) != str and type(user) != int:
            raise TypeError
        else:
            connected_users = []
            for record in self.get_records(str(user)):
                user1 = record.get_user()
                user2 = record.get_other_user()
                if (user1 not in connected_users) and (user1 != str(user)):
                    connected_users.append(user1)
                if (user2 not in connected_users) and (user2 != str(user)):
                    connected_users.append(user2)
            return connected_users

    def print_connection_matrix(self):
        """
        get a 2D list with which user is connected to who and the number of calls/messages between them

        :return: matrix : list
                 headers : list
        """
        matrix = []
        all_users = self.get_all_users()
        for u1 in all_users:
            connected_users = self.get_connected_users(u1)
            row = [u1]
            for u2 in all_users:
                if u2 in connected_users:
                    weight = len(self.get_records(u1, u2))
                    row.append(weight)
                else:
                    row.append(".")
            matrix.append(row)
        headers = all_users
        headers.insert(0, "")
        tools.print_matrix_new(matrix, headers)

    def get_connections(self, users=[], allow_duplicates=False):
        """
        returns a list of lists of [user1,user2]
        user1 makes a call to user2

        :return: connections : list
        """
        connections = set()
        connections_dup = []
        for record in self.get_records():
            if not users:
                connection, direction = [record.get_user(), record.get_other_user()], record.get_direction()
            else:
                u1 = record.get_user()
                u2 = record.get_other_user()
                if u1 in users or u2 in users:
                    connection, direction = [u1, u2], record.get_direction()
                else:
                    continue
            if direction == "Incoming":
                connection.reverse()
            if allow_duplicates:
                connections_dup.append(connection)
            else:
                connections.add(tuple(connection))
        if allow_duplicates:
            return connections_dup
        else:
            return connections

    def visualize_connection_network(self, directed=True, users=[], gui=False, fig_id='1', font_size=5):
        """
        Generates a graph with the connections within a given list of users.
        If the graph is directed the arrow head implies the direction of the call/message.
        The value near the arrow gives the number of connections made to that direction.

        :param fig_id: str
        :param gui: boolean
        :param directed: boolean
        :param users: list
                list of users
        :param font_size: int

        :return: connections : list
                 directed : boolean
        """
        connections = self.get_connections(users, allow_duplicates=True)
        weighted_edge_list = tools.get_weighted_edge_list(connections, directed)
        visualization.network_graph(weighted_edge_list, directed, gui, fig_id, font_size, users)

    def get_most_active_time(self, user):
        """
        Returns a dictionary with the hours in the day as keys and values as number of calls/messages made.

        :param user: string
                contact number of the user

        :return: active_time : dictionary
        """

        if type(user) != str and type(user) != int:
            raise TypeError
        else:
            keys = []
            for i in range(24):
                keys.append(i)
            active_time = {key: 0 for key in keys}
            for record in self.get_records(user1=str(user)):
                time = int(tools.get_datetime_from_timestamp(record.get_timestamp()).hour)
                active_time[time] += 1
            return active_time


class CallDataSet(CallMessageDataSet):

    def get_close_contacts(self, user, top_contact=5):
        """
        get top contacts who have most number of calls and longest call duration with a specific user

        :param user: string
                contact number of the user

        :param top_contact: int
                number of top close contacts

        :return: close_contacts : dictionary
        """
        if type(user) != str and type(user) != int:
            raise TypeError
        elif type(top_contact) != str and type(top_contact) != int:
            raise TypeError
        else:
            contacts_dict = {}
            user = str(user)
            for user2 in self.get_connected_users(user):
                valid_records = []
                for record in self.get_records(user, user2):
                    if int(record.get_duration()) > 0:
                        valid_records.append(record)
                contacts_dict[user2] = len(valid_records)
            close_contacts = dict(sorted(contacts_dict.items(), key=itemgetter(1), reverse=True)[:int(top_contact)])
            return close_contacts

    def get_call_records_by_antenna_id(self, cell_id):
        """
        get call records related to a specific cell

        :param cell_id: string/int

        :return: records : list
        """
        records = []
        for record in self.get_records():
            if record.get_cell_id() == str(cell_id):
                records.append(record)
        return records

    def get_ignored_call_details(self, user):
        """
        get ignored call details of a specific user

        :param user: string

        :return: ignored_call_records : list
        """
        if type(user) != str and type(user) != int:
            raise TypeError
        else:
            user = str(user)
            records = self.get_records(user1=user)
            ignored_call_records = []
            for record in records:
                if record.get_direction() == 'Incoming' and int(record.get_duration()) == 0:
                    date = tools.get_datetime_from_timestamp(record.get_timestamp())
                    call = {
                        'other user': record.get_other_user(),
                        'date': str(date.day).zfill(2) + '-' + str(date.month).zfill(2) + '-' + str(date.year),
                        'time stamp': str(date.hour).zfill(2) + ':' + str(date.minute).zfill(2) + ':' + str(
                            date.second).zfill(2),
                        'cell ID': record.get_cell_id()
                    }
                    ignored_call_records.append(call)
            return ignored_call_records


class MessageDataSet(CallMessageDataSet):

    def get_close_contacts(self, user, top_contact=5):
        """
        get top contacts who have most number of messages with a specific user

        :param user: string
                contact number of the user

        :param top_contact: int
                number of top close contacts

        :return: close_contacts : dictionary
        """
        if type(user) != str and type(user) != int:
            raise TypeError
        elif type(top_contact) != str and type(top_contact) != int:
            raise TypeError
        else:
            contacts_dict = {}
            for user2 in self.get_connected_users(str(user)):
                records = self.get_records(str(user), str(user2))
                contacts_dict[user2] = len(records)
            close_contacts = dict(sorted(contacts_dict.items(), key=itemgetter(1), reverse=True)[:int(top_contact)])
            return close_contacts


class CellDataSet(DataSet):
    def __init__(self, records, fieldnames, call_data_set):
        self._call_data_Set = call_data_set
        super().__init__(records, fieldnames)

    def get_cell_records(self, cell_id=None):
        """
        Get all cell records or specific cell record to a given cell id

        :param cell_id: int or None
        :return: cell record object(s)

        Example
        -------
        >> import cellyzer as cz
        >> call_file_path = "demo_datasets/test_data/calls.csv"
        >> antenna_file_path = "demo_datasets/test_data/antennas.csv"
        >> callDataSet = cz.read_call(call_file_path)
        >> antennaDataSet = cz.read_cell(antenna_file_path, call_dataset_obj=callDataSet, file_type='csv')
        >> record = antennaDataSet.get_cell_records(cell_id=1)
        """
        if cell_id is None:
            return self._records
        elif type(cell_id) != str and type(cell_id) != int and type(cell_id) != float:
            raise TypeError
        else:
            for record in self._records:
                if str(cell_id) == str(record.get_cell_id()):
                    return record

    def get_location(self, cell_id):
        """
        Get cell location tuple for a specific cell ID

        :param cell_id: int
        :return: tuple : (latitude, longitude)

        Example
        -------
        >> import cellyzer as cz
        >> call_file_path = "demo_datasets/test_data/calls.csv"
        >> antenna_file_path = "demo_datasets/test_data/antennas.csv"
        >> callDataSet = cz.read_call(call_file_path)
        >> antennaDataSet = cz.read_cell(antenna_file_path, call_dataset_obj=callDataSet, file_type='csv')
        >> location = antennaDataSet.get_location(cell_id = 1)
        """
        if type(cell_id) != str and type(cell_id) != int and type(cell_id) != float:
            raise TypeError
        else:
            antenna_record = self.get_cell_records(cell_id)
            if antenna_record is not None:
                location_tuple = (float(antenna_record.get_latitude()), float(antenna_record.get_longitude()))
                return location_tuple

    def get_population(self, cell_id=None):
        """
        get population around all the cells or around a given cell ID

        :param cell_id : int or None
        :return: dictionary : {'cell_id': 1,'latitude': 15.156464,'longitude': 15.16565,'population_around_cell': 50}

        Example
        -------
        >> import cellyzer as cz
        >> call_file_path = "demo_datasets/test_data/calls.csv"
        >> antenna_file_path = "demo_datasets/test_data/antennas.csv"
        >> callDataSet = cz.read_call(call_file_path)
        >> antennaDataSet = cz.read_cell(antenna_file_path, call_dataset_obj=callDataSet, file_type='csv')
        >> population = antennaDataSet.get_population()
        """

        if cell_id is None:
            population = []
            for record in self.get_cell_records():
                antenna_dict = self.get_population(cell_id=record.get_cell_id())
                population.append(antenna_dict)
            return population
        elif type(cell_id) != str and type(cell_id) != int and type(cell_id) != float:
            raise TypeError
        else:
            antenna_record = self.get_cell_records(cell_id)
            if antenna_record is not None:
                call_records = self._call_data_Set.get_call_records_by_antenna_id(cell_id)
                unique_users = self.get_unique_users_around_cell(call_records)
                no_of_homes_arround_cell = 0
                for user in unique_users:
                    if self.check_user_location_matches_cell(user, cell_id):
                        no_of_homes_arround_cell += 1

                antenna_dict = {'cell_id': cell_id,
                                'latitude': antenna_record.get_latitude(),
                                'longitude': antenna_record.get_longitude(),
                                'population_around_cell': no_of_homes_arround_cell
                                }
                return antenna_dict

    def get_unique_users_around_cell(self, call_records):
        # filter given call records to get unique user list
        unique_users = []
        for record in call_records:
            if record.get_user() not in unique_users:
                unique_users.append(record.get_user())
        return unique_users

    def check_user_location_matches_cell(self, contact_no, cell_id):
        # return true if user home location and given cell ID is equal
        # return false if user home location does not matches with the cell ID
        if type(cell_id) != str and type(cell_id) != int and type(cell_id) != float:
            raise TypeError
        elif type(contact_no) != str and type(contact_no) != int:
            raise TypeError
        else:
            contact_exist = False
            for call_record in self._call_data_Set.get_records():
                if str(call_record.get_user()) == str(contact_no):
                    contact_exist = True
                    break
            if contact_exist:
                user = User(self._call_data_Set, self, contact_no)
                if str(user.get_home_location_related_cell_id()) == str(cell_id):
                    return True
                else:
                    return False
            else:
                return False

    def get_trip_details(self, user, console_print=False, tabulate=False):
        """
        get/print/tabulate trip details of a specific user

        :param user: string
                contact number of a user

        :param console_print: boolean

        :param tabulate: boolean

        :return: sorted_trips : dictionary
        """
        if type(user) != str and type(user) != int:
            raise TypeError
        elif type(console_print) != bool or type(tabulate) != bool:
            raise TypeError
        else:
            trips = []
            user_records = self._call_data_Set.get_records(str(user))
            for record in user_records:
                trip = dict()
                if str(user) == record.get_user():
                    trip["timestamp"] = tools.get_datetime_from_timestamp(record.get_timestamp())
                    trip["duration"] = record.get_duration()
                    trip["cell_id"] = record.get_cell_id()
                    trip["location"] = self.get_location(record.get_cell_id())
                    trips.append(trip)
            sorted_trips = sorted(trips, key=itemgetter('timestamp'))
            if tabulate:
                utils.tabulate_list_of_dictionaries(sorted_trips)
            if console_print:
                print(sorted_trips)
            return sorted_trips


# class User
class User:
    def __init__(self, callDataSet, cellDataSet, contact_no, work_start_time=7, work_end_time=19):
        self._contact_no = str(contact_no)
        self._night_start = datetime.time(work_end_time)
        self._night_end = datetime.time(work_start_time)
        self._userCallDataSet = self.get_user_calldata(callDataSet)
        self.callDataSetObj = callDataSet
        self._cellDataSet = cellDataSet
        self._home = self.compute_home()
        self._work_location = self.compute_work_location()

    def get_contact_no(self):
        """
        Get user contact number

        :return: string

        Example
        -------
        >> call_file_path = "demo_datasets/test_data/calls.csv"
        >> antenna_file_path = "demo_datasets/test_data/antennas.csv"
        >> callDataSet = cz.read_call(call_file_path)
        >> cellDataSet = cz.read_cell(antenna_file_path)
        >> user_number = "xxxxxxxxx"
        >> user_obj = cz.User(callDataSet=callDataSet, cellDataSet=cellDataSet, contact_no=user_number)
        >> user_obj.get_contact_no()
        """
        return self._contact_no

    def get_user_calldata(self, calldataset):
        # return call data set of this user obj
        return calldataset.get_records(self._contact_no)

    def compute_home(self):
        # find the user home location and return -> [latitude , longitude]
        # if no records related to home - return work location  - assuming working at home
        location_dict = {}
        for call_record in self._userCallDataSet:
            at_home = self.check_timestamp_for_home(call_record)
            if at_home:
                cell_record = self._cellDataSet.get_cell_records(call_record.get_cell_id())
                location = str(cell_record.get_latitude()) + ',' + str(cell_record.get_longitude())
                if location in location_dict:
                    location_dict[location] += 1
                else:
                    location_dict[location] = 1
        if len(location_dict) > 0:
            latitude, longitude = map(float, max(location_dict, key=location_dict.get).split(','))
            home = [latitude, longitude]
            return home
        else:
            return self.compute_work_location()

    def compute_work_location(self):
        # find the user work location and return -> [latitude , longitude]
        # if no records related work location - return home location - assuming working from home
        location_dict = {}
        for call_record in self._userCallDataSet:
            at_work = not (self.check_timestamp_for_home(call_record))
            if at_work:
                cell_record = self._cellDataSet.get_cell_records(call_record.get_cell_id())
                location = str(cell_record.get_latitude()) + ',' + str(cell_record.get_longitude())
                if location in location_dict:
                    location_dict[location] += 1
                else:
                    location_dict[location] = 1
        if len(location_dict) > 0:
            latitude, longitude = map(float, max(location_dict, key=location_dict.get).split(','))
            work_place = [latitude, longitude]
            return work_place
        else:
            return self.compute_home()

    def check_timestamp_for_home(self, record):
        # return True if user call record is in the time period of staying home
        # else return False
        day = tools.get_index_of_day(record.get_timestamp())
        date = tools.get_datetime_from_timestamp(record.get_timestamp())
        if day > 5:  # weekend - at home
            return True
        else:  # weekday
            if self._night_start.hour >= date.hour > self._night_end.hour:  # at work place
                return False
            else:  # at home
                return True

    def get_home_location(self):
        """
        get home location of a user object

        :return: list : ['latitude' , 'longitude']

        Example
        -------
        >> call_file_path = "demo_datasets/test_data/calls.csv"
        >> antenna_file_path = "demo_datasets/test_data/antennas.csv"
        >> callDataSet = cz.read_call(call_file_path)
        >> cellDataSet = cz.read_cell(antenna_file_path)
        >> user_number = "xxxxxxxxx"
        >> user_obj = cz.User(callDataSet=callDataSet, cellDataSet=cellDataSet, contact_no=user_number)
        >> home_location = user_obj.get_home_location()
        """
        return self._home

    def get_work_location(self):
        """
        get work location of a user object

        :return: list : ['latitude' , 'longitude']

        Example
        -------
        >> call_file_path = "demo_datasets/test_data/calls.csv"
        >> antenna_file_path = "demo_datasets/test_data/antennas.csv"
        >> callDataSet = cz.read_call(call_file_path)
        >> cellDataSet = cz.read_cell(antenna_file_path)
        >> user_number = "xxxxxxxxx"
        >> user_obj = cz.User(callDataSet=callDataSet, cellDataSet=cellDataSet, contact_no=user_number)
        >> work_location = user_obj.get_work_location()
        """
        return self._work_location

    def get_home_location_related_cell_id(self):
        """
        get cell ID of the nearest cell to the home location

        :return: int : cell_id

        Example
        -------
        >> call_file_path = "demo_datasets/test_data/calls.csv"
        >> antenna_file_path = "demo_datasets/test_data/antennas.csv"
        >> callDataSet = cz.read_call(call_file_path)
        >> cellDataSet = cz.read_cell(antenna_file_path)
        >> user_number = "xxxxxxxxx"
        >> user_obj = cz.User(callDataSet=callDataSet, cellDataSet=cellDataSet, contact_no=user_number)
        >> home_location_cell = user_obj.get_home_location_related_cell_id()
        """

        for record in self._cellDataSet.get_cell_records():
            if float(record.get_latitude()) == self._home[0] and float(record.get_longitude()) == self._home[1]:
                return record.get_cell_id()

    def get_work_location_related_cell_id(self):
        """
        get cell ID of the nearest cell to the work location

        :return: int : cell_id

        Example
        -------
        >> call_file_path = "demo_datasets/test_data/calls.csv"
        >> antenna_file_path = "demo_datasets/test_data/antennas.csv"
        >> callDataSet = cz.read_call(call_file_path)
        >> cellDataSet = cz.read_cell(antenna_file_path)
        >> user_number = "xxxxxxxxx"
        >> user_obj = cz.User(callDataSet=callDataSet, cellDataSet=cellDataSet, contact_no=user_number)
        >> work_location_cell = user_obj.get_work_location_related_cell_id()
        """

        for record in self._cellDataSet.get_cell_records():
            if float(record.get_latitude()) == self._work_location[0] and float(record.get_longitude()) == \
                    self._work_location[1]:
                return record.get_cell_id()

    def get_ignored_call_details(self):
        """
        get user ignored call details

        :return: list of dictionaries
        """
        return self.callDataSetObj.get_ignored_call_details(self._contact_no)
