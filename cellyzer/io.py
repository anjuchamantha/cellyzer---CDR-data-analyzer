"""
Methods
---------
reading,writing datasets in many file types (csv,xlsx,txt)
altering datasets (removing columns etc.)

"""

import csv
import logging as log
from collections import OrderedDict
from dateutil.parser import parse
from datetime import datetime

from .core import DataSet, MessageDataSet, CallDataSet, Record, CallRecord, MessageRecord, CellRecord

log.getLogger().setLevel(log.WARN)


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

            for c in record_list:
                print(c)
            dataset_object = DataSet(record_list, fieldnames)
            return dataset_object

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

            # for c in call_list:
            #  print(c)

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
            user = other_user = direction = duration = timestamp = None

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

        filtered_call_records, bad_records = parse_records(call_records, fieldnames)
        call_dataset_obj = CallDataSet(filtered_call_records, fieldnames)

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
        filtered_message_records, bad_records = parse_records(msg_records, fieldnames)
        message_dataset_obj = MessageDataSet(filtered_message_records, fieldnames)

        # print("[x]  Objects creation successful\n")
        return message_dataset_obj


def filter_calls(call_records):
    def is_date(string, fuzzy=False):
        try:
            parse(string, fuzzy=fuzzy)
            return True

        except ValueError:
            return False

    def scheme(r):
        return {
            'user': True if len(r._user) != 0 and r._user.isdigit() else False,
            'other': True if len(r._other_user) != 0 and r._other_user.isdigit() else False,
            'direction': True if r._direction in ['Incoming', 'Outgoing', 'Missed'] else False,
            'duration': True if len(r._duration) != 0 and r._duration.isdigit() else False,
            'timestamp': is_date(r._timestamp),
        }

    ignored = OrderedDict([
        ('all', 0),
        ('user', 0),
        ('other', 0),
        ('direction', 0),
        ('duration', 0),
        ('timestamp', 0),
    ])

    bad_records = []

    def _filter(records):
        for r in records:
            valid = True
            for key, valid_key in scheme(r).items():
                if not valid_key:
                    ignored[key] += 1
                    bad_records.append(r)
                    # Not breaking, to count all fields with errors
                    valid = False

            if valid:
                yield r
            else:
                ignored['all'] += 1

    return list(_filter(call_records)), ignored, bad_records


def filter_messages(call_records):
    def is_date(string, fuzzy=False):
        try:
            parse(string, fuzzy=fuzzy)
            return True

        except ValueError:
            return False

    def scheme(r):
        return {
            'user': True if len(r._user) != 0 and r._user.isdigit() else False,
            'other': True if len(r._other_user) != 0 and r._other_user.isdigit() else False,
            'direction': True if r._direction in ['Incoming', 'Outgoing'] else False,
            'length': True if len(r._length) != 0 and r._length.isdigit() else False,
            'timestamp': is_date(r._timestamp),
        }

    ignored = OrderedDict([
        ('all', 0),
        ('user', 0),
        ('other', 0),
        ('direction', 0),
        ('length', 0),
        ('timestamp', 0),
    ])

    bad_records = []

    def _filter(records):
        for r in records:
            valid = True
            for key, valid_key in scheme(r).items():
                if not valid_key:
                    ignored[key] += 1
                    bad_records.append(r)
                    # Not breaking, to count all fields with errors
                    valid = False

            if valid:
                yield r
            else:
                ignored['all'] += 1

    return list(_filter(call_records)), ignored, bad_records


def parse_records(records, fieldnames):
    if 'duration' in fieldnames:
        filtered_records, ignored_list, bad_records = filter_calls(records)

    elif 'length' in fieldnames:
        filtered_records, ignored_list, bad_records = filter_messages(records)

    if ignored_list['all'] != 0:
        w = "{} record(s) were removed due to " \
            "missing or incomplete fields.".format(ignored_list['all'])
        for k in ignored_list.keys():
            if k != 'all' and ignored_list[k] != 0:
                w += "\n" + " " * 9 + "%s: %i record(s) with " \
                                      "incomplete values" % (k, ignored_list[k])
        print(w)
    print('End of parse_record function')

    return filtered_records, bad_records
