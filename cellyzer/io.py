"""
Methods
---------
reading,writing datasets in many file types (csv,xlsx,txt)
altering datasets (removing columns etc.)

"""

import csv
from collections import OrderedDict
from datetime import datetime

from .core import DataSet, MessageDataSet, CallDataSet, Record, CallRecord, MessageRecord, CellRecord


def io_func():
    print("I am from io")
    return


def read_csv(filepath):
    print("         from a CSV file ...")

    """
     Load records from a csv file.

    Parameters
    ----------
    path : str
        Path of the file.

    """
    try:
        with open(filepath, 'r') as csv_file:
            records = csv.DictReader(csv_file)

            fieldnames = records.fieldnames
            record_list = []
            for val in records:
                record = dict()
                for f in fieldnames:
                    record[f] = val[f]
                record_list.append(record)

            # for c in record_list:
            # print(c)

            filterrecords, bad_records, calldictionary, messagedictionary, celldictionary = filter_records(record_list,
                                                                                                           fieldnames)
            print(calldictionary)
            # dataset_object = DataSet(record_list, fieldnames)
            # return dataset_object

    except IOError:
        print("IO Error :", IOError)
        pass


def read_call(file_path):
    print("[x]  Reading Call Data")

    try:
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)

            fieldnames = reader.fieldnames
            call_list = []
            for val in reader:
                call = dict()
                for f in fieldnames:
                    call[f] = val[f]
                call_list.append(call)

            for c in call_list:
                print(c)

            create_call_obj(call_list, fieldnames)
    except IOError:
        print("IO Error :", IOError)
        pass

    """
     Load call records from a file.

    Parameters
    ----------
    path : str
        Path of the file.
        
    type : str
        Type of the file. (CSV,xls,json etc)
        
    
    """
    pass


def read_msg(file_path):
    # print("[x]  Reading Message Data...")

    try:
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)

            fieldnames = reader.fieldnames
            messages_list = []
            for val in reader:
                message = dict()
                for f in fieldnames:
                    message[f] = val[f]
                messages_list.append(message)

            return create_msg_obj(messages_list, fieldnames)
    except IOError:
        print("IO Error :", IOError)
        pass

    """
     Load message records from a file.

    Parameters
    ----------
    path : str
        Path of the file.

    type : str
        Type of the file. (CSV,xls,json etc)


    """


def read_cell():
    print("[x]  Reading Cell Data")
    read_csv()

    """
     Load cell records from a file.

    Parameters
    ----------
    path : str
        Path of the file.

    type : str
        Type of the file. (CSV,xls,json etc)


    """
    pass


def to_json():
    print("[x]  Writing to JSON file ...")
    pass


def to_csv():
    print("[x]  Writing to csv file ...")
    pass


def create_call_obj(calls, fieldnames):
    if calls is not None:

        call_records = []
        for call in calls:
            user = other_user = direction = duration = timestamp = antenna_id = cost = None

            for key in call:
                if 'user' == key:
                    user = call["user"]
                elif 'other' in key:
                    other_user = call[key]
                elif 'dir' in key:
                    direction = call[key]
                elif 'dur' in key:
                    duration = call[key]
                elif 'time' in key:
                    timestamp = call[key]
            # print(user, other_user, direction, length, timestamp)

            call_record_obj = CallRecord(
                user, other_user, direction, duration, timestamp)
            call_records.append(call_record_obj)
        call_dataset_obj = CallDataSet(call_records, fieldnames)

        # print("[x]  Objects creation successful\n")
        return call_dataset_obj


def create_msg_obj(messages, fieldnames):
    if messages is not None:

        msg_records = []
        for msg in messages:
            user = other_user = direction = length = timestamp = None

            for key in msg:
                if 'user' == key:
                    user = msg["user"]
                elif 'other' in key:
                    other_user = msg[key]
                elif 'dir' in key:
                    direction = msg[key]
                elif 'len' in key:
                    length = msg[key]
                elif 'time' in key:
                    timestamp = msg[key]
            # print(user, other_user, direction, length, timestamp)

            message_record_obj = MessageRecord(
                user, other_user, direction, length, timestamp)
            msg_records.append(message_record_obj)
        message_dataset_obj = MessageDataSet(msg_records, fieldnames)

        # print("[x]  Objects creation successful\n")
        return message_dataset_obj


def filter_records(records, fieldnames):
    def filter_calls(record):
        return {
            'user': isinstance(record['user'], int),
            'other': isinstance(record['other'], int),
            'direction': record['direction'] in ['incoming', 'outgoing'],
            'duration': isinstance(record['duration'], int),
            'timestamp': isinstance(record['timestamp'], datetime),
            'antenna_id': isinstance(record['antenna_id'], int),
            'cost': isinstance(record['cost'], int)
        }

    def filter_messages(r):
        return {
            'user': isinstance(r.user, int),
            'other': isinstance(r.other, int),
            'direction': r.direction in ['incoming', 'outgoing'],
            'length': isinstance(r.length, int),
            'timestamp': isinstance(r.timestamp, datetime),
        }

    def filter_cells(r):
        return {
            'antenna_id': isinstance(r.antenna_id, int),
            'latitude': isinstance(r.latitude, float),
            'longitude': isinstance(r.longitude, float)
        }

    # calldictionary = {"all": 0, "user": 0, "other": 0, "direction": 0, "duration": 0, "timestamp": 0, "antenna_id": 0,
                      # "cost": 0}
    messagedictionary = {"all": 0, "user": 0, "other": 0, "direction": 0, "length": 0, "timestamp": 0}
    celldictionary = {"all": 0, "antenna_id": 0, "latitude": 0, "longitude": 0}
    bad_records = []

    calldictionary = OrderedDict([
        ('all', 0),
        ('user', 0),
        ('other', 0),
        ('direction', 0),
        ('duration', 0),
        ('timestamp', 0),
        ('antenna_id', 0),
        ('cost', 0),
    ])

    def _filter(records, fieldnames):
        if 'duration' in fieldnames:
            for record in records:
                valid = True
                print(record)
                for key, valid_key in filter_calls(record).items():
                    if not valid_key:
                        calldictionary[key] += 1
                        bad_records.append(record)
                        # Not breaking, to count all fields with errors
                        valid = False

                    if valid:
                        yield record
                    else:
                        calldictionary["all"] += 1

        elif 'length' in fieldnames:
            for record in records:
                valid = True
                for key, valid_key in filter_messages(record).items:
                    if not valid_key:
                        messagedictionary[key] += 1
                        bad_records.append(record)
                        # Not breaking, to count all fields with errors
                        valid = False

                    if valid:
                        yield record
                    else:
                        messagedictionary["all"] += 1

        elif 'antenna_id' in fieldnames:
            for record in records:
                valid = True
                for key, valid_key in filter_cells(record).items:
                    if not valid_key:
                        celldictionary[key] += 1
                        bad_records.append(record)
                        # Not breaking, to count all fields with errors
                        valid = False

                    if valid:
                        yield record
                    else:
                        celldictionary["all"] += 1

    return list(_filter(records, fieldnames)), bad_records, calldictionary, messagedictionary, celldictionary
