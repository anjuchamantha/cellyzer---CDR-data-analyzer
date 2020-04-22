"""
Methods
---------
reading,writing datasets in many file types (csv,xlsx,txt)
altering datasets (removing columns etc.)

"""

import csv
import xlrd
import json
import logging as log
from collections import OrderedDict
from json import dumps
import hashlib

from dateutil.parser import parse
from datetime import datetime

from .core import DataSet, MessageDataSet, CallDataSet, CellDataSet, Record, CallRecord, MessageRecord, CellRecord
from .tools import ColorHandler
from .utils import flatten

log.getLogger().setLevel(log.WARN)
log.getLogger().addHandler(ColorHandler())


def io_func():
    print("I am from io")
    return


def to_json(dataset_object, filename):
    print("[x]  Writing to JSON file ...")

    """
         write dataset object to a json file.

        Parameters
        ----------
        objects : list
            List of objects to be exported.
        filename : string
            File to export to.

        """

    if '.JSON' or '.json' not in filename:
        filename = filename + '.json'

    i = 0
    records = dataset_object.get_records()
    obj_dict = OrderedDict([('Record:' + str(records.index(obj)), obj) for obj in records])

    with open(filename, 'w') as f:
        f.write(dumps(obj_dict, indent=4, separators=(',', ': ')))

    print("Successfully exported {} object(s) to {}".format(len(records),
                                                            filename))


def to_csv(dataset_object, filename):
    print("[x]  Writing to CSV file ...")

    """
            write dataset object to a csv file.

            Parameters
            ----------
            objects : list
                List of objects to be exported.
            filename : string
                File to export to.

            """

    data = [flatten(obj) for obj in dataset_object.get_records()]
    fieldnames = dataset_object.fieldnames

    if '.csv' not in filename:
        filename = filename + '.csv'

    with open(filename, 'w') as f:
        w = csv.writer(f)
        w.writerow(fieldnames)

        def make_repr(item):
            if item is None:
                return None
            elif isinstance(item, float):
                return repr(round(item, 5))
            else:
                return str(item)

        for row in data:
            row = dict((k, make_repr(v)) for k, v in row.items())
            w.writerow([make_repr(row.get(k, None)) for k in fieldnames])

    print("Successfully exported {} object(s) to {}".format(len(dataset_object.get_records()),
                                                            filename))


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


def read_call(file_path, file_type='csv', hash=True):
    print("[x]  Reading Call Data")

    """
     Load call records from a file.

    Parameters
    ----------
    path : str
        Path of the file.

    type : str
        Type of the file. (CSV,xls,json etc)


    """

    try:
        if file_type.lower() == 'csv':
            # dataset_object = read_csv(file_path)
            # return create_call_obj(dataset_object.get_records(), dataset_object.fieldnames)
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
                return create_call_obj(call_list, fieldnames, hash)
        elif file_type.lower() == 'xls' or file_type.lower() == 'xlsx':
            return read_xls(file_path)
        elif file_type.lower() == 'json':
            return read_json(file_path)
        else:
            print('Invalid Format')
    except IOError:
        print("IO Error :", IOError)
        pass


def read_msg(file_path, file_type='csv', hash=True):
    print("[x]  Reading Message Data...")

    """
     Load message records from a file.

    Parameters
    ----------
    path : str
        Path of the file.

    type : str
        Type of the file. (CSV,xls,json etc)


    """

    try:
        if file_type.lower() == 'csv':
            with open(file_path, 'r') as csv_file:
                reader = csv.DictReader(csv_file)

                fieldnames = reader.fieldnames
                messages_list = []
                for val in reader:
                    message = dict()
                    for f in fieldnames:
                        message[f] = val[f]
                    messages_list.append(message)

                return create_msg_obj(messages_list, fieldnames, hash)
        elif file_type.lower() == 'xls' or file_type.lower() == 'xlsx':
            return read_xls(file_path)
        elif file_type.lower() == 'json':
            return read_json(file_path)
        else:
            print('Invalid Format')
    except IOError:
        print("IO Error :", IOError)
        pass


def read_cell(file_path, call_csv_path=None, call_dataset_obj=None, file_type='csv'):
    # print("[x]  Reading Cell Data")

    """
    Load cell records from a file.

    Parameters
    ----------
    path : str
        Path of the file.

    type : str
        Type of the file. (CSV,xls,json etc)


    """
    try:
        if file_type.lower() == 'csv':
            with open(file_path, 'r') as csv_file:
                reader = csv.DictReader(csv_file)

                fieldnames = reader.fieldnames
                cell_list = []
                for val in reader:
                    cell = dict()
                    for f in fieldnames:
                        cell[f] = val[f]
                    cell_list.append(cell)
                if call_csv_path is not None:
                    call_data_set = read_call(call_csv_path)
                if call_dataset_obj is not None:
                    call_data_set = call_dataset_obj
                else:
                    call_data_set = None
                return create_cell_obj(cell_list, fieldnames, call_data_set)
        elif file_type.lower() == 'xls' or file_type.lower() == 'xlsx':
            if call_csv_path is not None:
                call_data_set = read_call(call_csv_path, 'xls')
            if call_dataset_obj is not None:
                call_data_set = call_dataset_obj
            else:
                call_data_set = None
            return read_xls(file_path, call_data_set)
        elif file_type.lower() == 'json':
            return read_json(file_path)
        else:
            print('Invalid Format')
    except IOError:
        print("IO Error :", IOError)
        pass


def read_xls(filepath, call_data_set=None):
    print("[x]  Reading Data From Excel File")

    """
    Load records from a excel file.

    Parameters
    ----------
    path : str
        Path of the file.

    """
    sample, fieldnames = xls_to_dict(filepath)
    _level = log.getLogger().level
    if 'latitude' in fieldnames and len(fieldnames) == 3:
        return create_cell_obj(sample, fieldnames, call_data_set)
    elif 'duration' in fieldnames and len(fieldnames) == 7:
        return create_call_obj(sample, fieldnames)
    elif 'length' in fieldnames and len(fieldnames) == 5:
        return create_msg_obj(sample, fieldnames)
    else:
        log.warning('Invalid Input')
        log.getLogger().setLevel(_level)


def read_json(filepath):
    print("[x]  Reading Data From JSON File")

    """

    Parameters
    ----------
    path : str
        Path of the file.

    """
    record_list = []
    try:
        with open(filepath) as json_file:
            try:
                data = json.load(json_file)
                for key in data:
                    if key.lower() == 'callrecords':
                        fieldnames = data[key][0].keys()
                        for records in data[key]:
                            record_list.append(records)
                        print(record_list)
                        return create_call_obj(record_list, fieldnames)
                    elif key.lower() == 'messagerecords':
                        fieldnames = data[key][0].keys()
                        for records in data[key]:
                            record_list.append(records)
                        print(record_list)
                        return create_msg_obj(record_list, fieldnames)
                    elif key.lower() == 'cellrecords':
                        fieldnames = data[key][0].keys()
                        for records in data[key]:
                            record_list.append(records)
                        print(record_list)
                        return create_cell_obj(record_list, fieldnames)
                    else:
                        log.warning("This File Has Invalid Inputs")
            except ValueError:  # includes simplejson.decoder.JSONDecodeError
                print('Decoding JSON has failed. Please Check The JSON File Again')
    except IOError:
        print("IO Error :", IOError)
        pass


def hash_number(number):
    last3 = number[-3:]
    hash_val = str(hashlib.sha224(number[:7].encode()).hexdigest())
    # print(hash_val[:6] + last3)
    return hash_val[:7] + last3


def create_call_obj(calls, fieldnames, hash):
    if calls is not None:

        call_records = []
        for call in calls:
            user = other_user = direction = duration = timestamp = cell_id = cost = None

            for key in call:
                if 'user' in key:
                    if hash:
                        user = hash_number(call["user"])
                    else:
                        user = call["user"]
                elif 'other' in key:
                    if hash:
                        other_user = hash_number(call[key])
                    else:
                        other_user = call[key]
                elif 'dir' in key:
                    direction = call[key]
                elif 'dur' in key:
                    duration = call[key]
                elif 'time' in key:
                    timestamp = call[key]
                elif 'cell' in key or 'antenna' in key:
                    cell_id = call[key]
                elif 'cost' in key:
                    cost = call[key]

            # print(user, other_user, direction, length, timestamp)

            call_record_obj = CallRecord(
                user, other_user, direction, duration, timestamp, cell_id, cost)
            call_records.append(call_record_obj)

        filtered_call_records, bad_records = parse_records(call_records, fieldnames)
        call_dataset_obj = CallDataSet(filtered_call_records, fieldnames)

        print("[x]  Objects creation successful\n")
        return call_dataset_obj


def create_msg_obj(messages, fieldnames, hash):
    if messages is not None:

        msg_records = []
        for msg in messages:
            user = other_user = direction = length = timestamp = None

            for key in msg:
                if 'user' in key:
                    if hash:
                        user = hash_number(msg[key])
                    else:
                        user = msg[key]
                elif 'other' in key:
                    if hash:
                        other_user = hash_number(msg[key])
                    else:
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

        print("[x]  Objects creation successful\n")
        return message_dataset_obj


def create_cell_obj(cells, fieldnames, call_data_set):
    if cells is not None:

        cell_records = []
        for cell in cells:
            cell_id = latitude = longitude = None

            for key in cell:
                if 'antenna_id' in key or 'cell_id' in key:
                    cell_id = cell[key]
                elif 'latitude' in key:
                    latitude = cell[key]
                elif 'longitude' in key:
                    longitude = cell[key]

            cell_record_obj = CellRecord(
                cell_id, latitude, longitude
            )
            cell_records.append(cell_record_obj)
        filtered_cell_records, bad_records = parse_records(cell_records, fieldnames)
        cell_dataset_obj = CellDataSet(filtered_cell_records, fieldnames, call_data_set)
        return cell_dataset_obj


def filter_calls(call_records):
    def is_date(string, fuzzy=False):
        try:
            parse(string, fuzzy=fuzzy)
            return True

        except ValueError:
            return False

    def scheme(r):
        return {
            'user': True if len(r.user) != 0 else False,
            'other': True if len(r.other_user) != 0 else False,
            'direction': True if r.direction in ['Incoming', 'Outgoing', 'Missed'] else False,
            'duration': True if len(r.duration) != 0 and r.duration.isdigit() else False,
            'timestamp': is_date(r.timestamp),
            'cell_id': True if len(r.cell_id) != 0 and r.cell_id.isdigit() else False,
            'cost': True if len(r.cost) != 0 and r.cost.isdigit() else False,
        }

    ignored = OrderedDict([
        ('all', 0),
        ('user', 0),
        ('other', 0),
        ('direction', 0),
        ('duration', 0),
        ('timestamp', 0),
        ('cell_id', 0),
        ('cost', 0),
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
            'user': True if len(r._user) != 0 else False,
            'other': True if len(r._other_user) != 0 else False,
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


def filter_cells(cell_records):
    def is_float(string):
        if '-' in string:
            try:
                if float(string[1:]) and not string[1:].isdigit():
                    return True
                else:
                    return False
            except ValueError:
                return False
        else:
            try:
                if float(string) and not string.isdigit():
                    return True
                else:
                    return False
            except ValueError:
                return False

    def scheme(r):
        return {
            'cell_id': True if len(r._cell_id) != 0 and r._cell_id.isdigit() else False,
            'latitude': True if len(r._latitude) != 0 and is_float(r._latitude) else False,
            'longitude': True if len(r._longitude) != 0 and is_float(r._longitude) else False,
        }

    ignored = OrderedDict([
        ('all', 0),
        ('cell_id', 0),
        ('latitude', 0),
        ('longitude', 0),
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

    return list(_filter(cell_records)), ignored, bad_records


def parse_records(records, fieldnames):
    _level = log.getLogger().level
    if 'duration' in fieldnames:
        filtered_records, ignored_list, bad_records = filter_calls(records)

    elif 'length' in fieldnames:
        filtered_records, ignored_list, bad_records = filter_messages(records)

    elif 'latitude' in fieldnames:
        filtered_records, ignored_list, bad_records = filter_cells(records)

    if ignored_list['all'] != 0:
        w = "{} record(s) were removed due to " \
            "missing or incomplete fields.".format(ignored_list['all'])
        for k in ignored_list.keys():
            if k != 'all' and ignored_list[k] != 0:
                w += "\n" + " " * 9 + "%s: %i record(s) with " \
                                      "incomplete values" % (k, ignored_list[k])
        log.warning(w)
    log.getLogger().setLevel(_level)
    return filtered_records, bad_records


def make_json_from_data(column_names, row_data):
    row_list = []
    for item in row_data:
        json_obj = {}
        for i in range(0, column_names.__len__()):
            json_obj[column_names[i]] = item[i]
        row_list.append(json_obj)
    return row_list


def xls_to_dict(workbook_url):
    book = xlrd.open_workbook(workbook_url)
    sheet = book.sheet_by_index(0)

    columns = sheet.row_values(0)
    rows = []
    for row_index in range(1, sheet.nrows):
        row = sheet.row_values(row_index)
        filteredlist = float_to_int(row)
        rows.append(filteredlist)
    sheet_data = make_json_from_data(columns, rows)
    print(sheet_data)
    return sheet_data, columns


def float_to_int(listobject):
    newlist = []
    for object in listobject:
        try:
            splittedobject = str(object).split('.')
            if splittedobject[1] == '0':
                newlist.append(splittedobject[0])
            else:
                newlist.append(str(object))
        except IndexError:
            newlist.append(object)
    return newlist
