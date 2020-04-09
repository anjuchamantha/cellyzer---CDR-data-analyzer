"""
Main classes are modeled here

"""

from operator import itemgetter

from . import tools
from . import visualization


# Classes for Records
class Record:
    pass


class CallRecord(Record):

    def __init__(self, user, other_user, direction, duration, timestamp, cell_id, cost):
        self._user = user
        self._other_user = other_user
        self._direction = direction
        self._duration = duration
        self._timestamp = timestamp
        self._cell_id = cell_id
        self._cost = cost

    def get_user(self):
        return self._user

    def get_other_user(self):
        return self._other_user

    def get_direction(self):
        return self._direction

    def get_duration(self):
        return self._duration

    def get_timestamp(self):
        return self._timestamp

    def get_cell_id(self):
        return self._cell_id

    def get_cost(self):
        return self._cost


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
        self.fieldnames = fieldnames
        if records is None:
            self._records = []
        else:
            self._records = records

    def add_records(self, data):
        self._records.append(data)

    def get_max(self):
        return self._records

    def get_columns(self):
        print("columns")

    def get_rows(self):
        print("rows")

    def get_all_users(self):
        # return all the different users in the CallDataSet
        all_users = []
        for record in self.get_records():
            user = record.get_user()
            other_user = record.get_other_user()
            if user not in all_users:
                all_users.append(user)
            if other_user not in all_users:
                all_users.append(other_user)
        return all_users

    def get_records(self, user1=None, user2=None):
        # filter records using given user(s)
        records = []
        if (user1 is None) and (user2 is None):
            # calls the function of Dataset class
            # return all the records : List of Record objects
            return self._records

        for record in self._records:
            user = record.get_user()
            other_user = record.get_other_user()
            if (user1 is not None) and (user2 is None):
                # returns a list of Record objects where the given user is involved
                if user1 == user or user1 == other_user:
                    records.append(record)
            if (user1 is not None) and (user2 is not None):
                # returns a list of Record objects where the given 2 users are involved
                if (user1 == user and user2 == other_user) or (user1 == other_user and user2 == user):
                    records.append(record)
        return records

    def get_connected_users(self, user):
        # returns the list of users that are connected to the given user
        connected_users = []
        for record in self.get_records(user):
            user1 = record.get_user()
            user2 = record.get_other_user()
            if (user1 not in connected_users) and (user1 != user):
                connected_users.append(user1)
            if (user2 not in connected_users) and (user2 != user):
                connected_users.append(user2)
        return connected_users

    def print_connection_matrix(self):
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
        tools.print_matrix(matrix, headers)
        return matrix, headers

    def get_connections(self):
        # returns a list of lists of [user1,user2]
        # user1 makes a call to user2
        connections = []
        for record in self.get_records():
            connection, direction = [record.get_user(), record.get_other_user()], record.get_direction()
            if direction == "Incoming":
                connection.reverse()
            connections.append(connection)
        return connections

    def visualize_connection_network(self, directed=True):
        connections = self.get_connections()
        weighted_edge_list = tools.get_weighted_edge_list(connections, directed)
        visualization.network_graph(weighted_edge_list, directed)
        return connections, directed

    def get_close_contacts(self, user, top_contact=5):
        # get top contacts who have most number of calls and longest call duration with the user
        contacts_dict = {}
        for user2 in self.get_connected_users(user):
            valid_records = []
            for record in self.get_records(user, user2):
                if int(record.get_duration()) > 0:
                    valid_records.append(record)
            contacts_dict[user2] = len(valid_records)
        close_contacts = dict(sorted(contacts_dict.items(), key=itemgetter(1), reverse=True)[:top_contact])
        return close_contacts


class CallDataSet(DataSet):
    def get_most_active_time(self, user):
        keys = []
        for i in range(24):
            keys.append(i)
        active_time = {key: 0 for key in keys}
        for record in self.get_records(user1=user):
            time = int(record.get_timestamp().split()[3][:2])
            active_time[time] += 1
        return active_time

    def get_call_records_by_antenna_id(self, cell_id):
        records = []
        for record in self.get_records():
            if record.get_cell_id() == str(cell_id):
                records.append(record)
        return records

    def get_call_details(self):
        print("call details")


class MessageDataSet(DataSet):
    def get_frequenct_conversations(self):
        print("Frequent conversations between ")


class CellDataSet(DataSet):
    def get_cell_records(self, cell_id=None):
        if cell_id is None:
            return self._records
        else:
            for record in self._records:
                if int(cell_id) == int(record.get_cell_id()):
                    return record

    def get_population(self, callDataset, cell_id=None):
        if cell_id is None:
            population = []
            for record in self.get_cell_records():
                antenna_dict = self.get_population(callDataset, cell_id=record.get_cell_id())
                population.append(antenna_dict)
            return population
        else:
            antenna_record = self.get_cell_records(cell_id)
            call_records = callDataset.get_call_records_by_antenna_id(cell_id)
            antenna_dict = {'cell_id': cell_id,
                            'latitude': antenna_record.get_latitude(),
                            'longitude': antenna_record.get_longitude(),
                            'population_around_cell': len(call_records)
                            }
            return antenna_dict


# class User
class User:
    def __init__(self, contact_no):
        self._contact_no = contact_no

    def get_contact_no(self):
        return self._contact_no

    def get_trip(self):
        print("trips")

    def get_home_location(self):
        print("home location = xxx . xxx")

    def get_work_location(self):
        print("work location = xxx . xxx")

    def get_ignored_calls(self):
        print("ignored calls = 111222333")
