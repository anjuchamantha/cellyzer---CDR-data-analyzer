"""
Main classes are modeled here

classes
---------
CallRecord
User
Message
Cell

"""

import matplotlib.pyplot as plt
import numpy as np
import math


# class DataFrame:
#     def __init__(self):


# Classes for Records
class Record:
    def getsomething(self):
        print ("in parent record class")


class CallRecord(Record):

    def __init__(self, user, other_user, direction, duration, timestamp):
        self._user = user,
        self._other_user = other_user
        self._direction = direction,
        self._duration = duration,
        self._timestamp = timestamp

    def get_user(self):
        return self._user

    def get_other_user(self):
        return self._other_user

    def get_direction(self):
        return self._direction

    def get_duration(self):
        return self._direction

    def get_timestamp(self):
        return self._timestamp


class MessageRecord(Record):

    def __init__(self, user, other_user, direction, length, timestamp):
        self._user = user,
        self._other_user = other_user
        self._direction = direction,
        self._length = length,
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
        self._cell_id = cell_id,
        self._latitude = latitude,
        self._longitude = longitude

    def get_cell_id(self):
        return self._cell_id

    def get_latitude(self):
        return self._latitude

    def get_longitude(self):
        return self._longitude


# classes for DataSet
class DataSet:
    def __init__(self):
        self._records = []

    # def get_records(self):
    #     return self._records

    def add_data_to_records(self, data):
        self._records.append(data)

    def get_max(self):
        return self._records

    def get_columns(self):
        print ("columns")

    def get_rows(self):
        print ("rows")


class CallDataSet(DataSet):
    def get_close_contacts(self):
        print("close contacts")

    def get_most_active_time(self):
        print ("most active time")

    def get_call_details(self):
        print ("call details")

class MessageDataSet(DataSet):
    def get_close_contacts(self):
        print("close contacts")

    def get_frequenct_conversations(self):
        print("frequent conversations")


class CellDataSet(DataSet):
    def get_population(self , cell_id):
        print("close contacts around = ", cell_id)


# class User
class User:
    def __init__(self, contact_no):
        self._contact_no = contact_no

    def get_contact_no(self):
        return self._contact_no

    def get_trip(self):
        print ("trips")

    def get_home_location(self):
        print ("home location = xxx . xxx")

    def get_work_location(self):
        print ("work location = xxx . xxx")

    def get_ignored_calls(self):
        print ("ignored calls = 111222333")


# additional functions
def graph():
    x = np.arange(0, math.pi * 2, 0.05)
    y = np.sin(x)
    plt.xlabel("angle")
    plt.ylabel("sine")
    plt.title("Sine Wave")
    plt.plot(x, y)
    plt.show()
    return
