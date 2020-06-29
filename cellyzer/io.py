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

from .core import DataSet, MessageDataSet, CallDataSet, CellDataSet, Record, CallRecord, MessageRecord, CellRecord
from .tools import ColorHandler
from .utils import flatten

log.getLogger().setLevel(log.WARN)
log.getLogger().addHandler(ColorHandler())


def to_json(dataset_object, filename):
    """
    Write dataset object to a json file
    :param dataset_object: dataset object created
    :param filename: name of the dataset file
    :return: None
    """
    instance_type = type(dataset_object).__name__
    if instance_type != "CallDataSet" and instance_type != "MessageDataSet" and instance_type != "CellDataSet":
        raise TypeError
    elif type(filename) != str:
        raise TypeError
    else:
        print("[x]  Writing to JSON file ...")

        if '.JSON' or '.json' not in filename:
            filename = filename + '.json'

        i = 0
        records = dataset_object.to_dict()
        obj_dict = OrderedDict([('Record:' + str(records.index(obj)), obj) for obj in records])

        with open(filename, 'w') as f:
            f.write(dumps(obj_dict, indent=4, separators=(',', ': ')))

        print("Successfully exported {} object(s) to {}".format(len(records),
                                                                filename))


def to_csv(dataset_object, filename):
    """
    Write a dataset object to a csv file
    :param dataset_object: dataset object created
    :param filename: name of the dataset file
    :return: None
    """
    instance_type = type(dataset_object).__name__
    if instance_type != "CallDataSet" and instance_type != "MessageDataSet" and instance_type != "CellDataSet":
        raise TypeError
    elif type(filename) != str:
        raise TypeError
    else:
        print("[x]  Writing to CSV file ...")

        data = [flatten(obj) for obj in dataset_object.to_dict()]
        'fieldnames = dataset_object.get_fieldnames()'
        if instance_type == "CallDataSet":
            fieldnames = ["_user", "_other", "_direction", "_duration", "_timestamp", "_antenna_id", "_cost"]
        elif instance_type == "MessageDataSet":
            fieldnames = ["_user", "_other", "_direction", "_length", "_timestamp"]
        elif instance_type == "CellDataSet":
            fieldnames = ["_antenna_id","_latitude","_longitude"]

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
                print(row)
                w.writerow([make_repr(row.get(k, None)) for k in fieldnames])

        print("Successfully exported {} object(s) to {}".format(len(dataset_object.get_records()),
                                                                filename))


def read_csv(filepath):
    """
     Load records from a csv file.

    Parameters
    ----------
    path : str
        Path of the file.

    """
    if type(filepath) != str:
        raise TypeError
    else:
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
                dataset_object = DataSet(record_list, fieldnames)

                return dataset_object

        except IOError:
            print("IO Error :", IOError)
            pass


def read_call(file_path="", file_type='csv', hash=True, decode_read="", splitted_line=None):
    """
    Loads call records dataset and returns a call dataset object
    :param file_path: file path of the dataset
    :param file_type: csv,xlsx,json file types are accepted
    :param hash: hash user phone numbers for privacy
    :return: CallDataset object
    """
    print("[x]  Reading Call Data")

    if type(file_path) != str or type(file_type) != str or type(hash) != bool:
        raise TypeError
    elif type(splitted_line) != list and splitted_line is not None:
        raise TypeError
    else:
        if not (decode_read == ""):
            data_list = decode_read.getvalue().split('\r\n')
            fieldnames = data_list[0].split(',')
            call_list = []
            for line in data_list[1:len(data_list) - 1]:
                splitted_line = line.split(',')
                call = dict()
                i = 0
                for f in fieldnames:
                    if splitted_line[i] is not None:
                        call[f] = splitted_line[i]
                    else:
                        call[f] = ''
                    i += 1
                call_list.append(call)
            return create_call_obj(call_list, fieldnames, hash)

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
                    return create_call_obj(call_list, fieldnames, hash)
            elif file_type.lower() == 'xls' or file_type.lower() == 'xlsx':
                return read_xls(file_path, hash)
            elif file_type.lower() == 'json':
                return read_json(file_path, hash)
            else:
                print('Invalid Format')
        except IOError:
            print("IO Error :", IOError)
            pass


def read_msg(file_path='', file_type='csv', hash=True, decode_read="", splitted_line=None):
    """
    Loads message records dataset and returns a message dataset object
    :param file_path: file path of the dataset
    :param file_type: csv,xlsx,json file types are accepted
    :param hash: hash user phone numbers for privacy
    :return: MessageDataset object
    """
    print("[x]  Reading Message Data...")

    if type(file_path) != str or type(file_type) != str or type(hash) != bool:
        raise TypeError
    elif type(splitted_line) != list and splitted_line is not None:
        raise TypeError
    else:
        if not (decode_read == ""):
            data_list = decode_read.getvalue().split('\r\n')
            fieldnames = data_list[0].split(',')
            msg_list = []
            for line in data_list[1:len(data_list) - 1]:
                splitted_line = line.split(',')
                msg = dict()
                i = 0
                for f in fieldnames:
                    if splitted_line[i] is not None:
                        msg[f] = splitted_line[i]
                    else:
                        msg[f] = ''
                    i += 1
                msg_list.append(msg)
            return create_msg_obj(msg_list, fieldnames, hash)

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
                return read_xls(file_path, hash)
            elif file_type.lower() == 'json':
                return read_json(file_path, hash)
            else:
                print('Invalid Format')
        except IOError:
            print("IO Error :", IOError)
            pass


def read_cell(file_path='', call_csv_path=None, call_dataset_obj=None, file_type='csv', decode_read="",
              splitted_line=None):
    """
    Loads cell dataset and returns a cell dataset. In order to adda a cell-dataset,
     a call dataset object or call dataset filepath is also needed

    :param file_path: file path of the dataset
    :param call_csv_path: file path of the call dataset
    :param call_dataset_obj: call dataset object
    :param file_type: csv,xlsx,json file types are accepted
    :return: CellDataset object
    """
    print("[x]  Reading Cell Data")

    if type(file_path) != str or type(file_type) != str:
        raise TypeError
    elif type(call_csv_path) != str and call_csv_path is not None:
        raise TypeError
    elif type(call_dataset_obj).__name__ != "CallDataSet" and call_dataset_obj is not None:
        raise TypeError
    elif type(splitted_line) != list and splitted_line is not None:
        raise TypeError
    else:
        if not (decode_read == ""):
            data_list = decode_read.getvalue().split('\r\n')
            fieldnames = data_list[0].split(',')
            cell_list = []
            if call_csv_path is not None:
                call_data_set = read_call(call_csv_path)
            if call_dataset_obj is not None:
                call_data_set = call_dataset_obj
            else:
                call_data_set = None
            for line in data_list[1:len(data_list) - 1]:
                splitted_line = line.split(',')
                cell = dict()
                i = 0
                for f in fieldnames:
                    if splitted_line[i] is not None:
                        cell[f] = splitted_line[i]
                    else:
                        cell[f] = ''
                    i += 1
                cell_list.append(cell)
            return create_cell_obj(cell_list, fieldnames, call_data_set)

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
                if call_csv_path is not None:
                    call_data_set = read_call(call_csv_path, 'xls')
                if call_dataset_obj is not None:
                    call_data_set = call_dataset_obj
                else:
                    call_data_set = None
                return read_json(file_path, call_data_set)
            else:
                print('Invalid Format')
        except IOError:
            print("IO Error :", IOError)
            pass


def read_xls(filepath, call_data_set=None, hash=True):
    """
    Read a dataset from a excel file
    :param filepath: path of the dataset file
    :return:
    """
    print("[x]  Reading Data From Excel File")

    if type(filepath) != str or type(hash) != bool:
        raise TypeError
    else:
        sample, fieldnames = xls_to_dict(filepath)
        _level = log.getLogger().level
        if 'latitude' in fieldnames and len(fieldnames) == 3:
            return create_cell_obj(sample, fieldnames, call_data_set)
        elif 'duration' in fieldnames and len(fieldnames) == 7:
            return create_call_obj(sample, fieldnames, hash)
        elif 'length' in fieldnames and len(fieldnames) == 5:
            return create_msg_obj(sample, fieldnames, hash)
        else:
            log.warning('Invalid Input')
            log.getLogger().setLevel(_level)


def read_json(filepath, call_data_set=None, hash=True):
    print("[x]  Reading Data From JSON File")

    """

    Parameters
    ----------
    path : str
        Path of the file.

    """
    if type(filepath) != str or type(hash) != bool:
        raise TypeError
    else:
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
                            return create_call_obj(record_list, fieldnames, hash)
                        elif key.lower() == 'messagerecords':
                            fieldnames = data[key][0].keys()
                            for records in data[key]:
                                record_list.append(records)
                            return create_msg_obj(record_list, fieldnames, hash)
                        elif key.lower() == 'cellrecords':
                            fieldnames = data[key][0].keys()
                            for records in data[key]:
                                record_list.append(records)
                            return create_cell_obj(record_list, fieldnames, call_data_set)
                        else:
                            log.warning("This File Has Invalid Inputs")
                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    print('Decoding JSON has failed. Please Check The JSON File Again')
        except IOError:
            print("IO Error :", IOError)
            pass


def hash_number(number):
    if type(number) != str and type(number) != int and type(number) != float:
        raise TypeError
    else:
        number = str(number)
        last3 = number[-3:]
        hash_val = str(hashlib.sha224(number[:7].encode()).hexdigest())
        return hash_val[:7] + last3


def create_call_obj(calls, fieldnames, hash):
    if type(calls) != list or type(hash) != bool:
        raise TypeError
    elif calls is not None:
        call_records = []
        for i in range(0, len(calls)):
            call = calls[i]
            user = other_user = direction = duration = timestamp = cell_id = cost = None

            for key in call:
                if not isinstance(call[key], str):
                    call[key] = str(call[key])
                if 'user' in key:
                    if hash and call['user'] != '':
                        user = hash_number(str(call["user"]))
                    else:
                        user = call["user"]
                elif 'other' in key:
                    if hash and call['other'] != '':
                        other_user = hash_number(str(call[key]))
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

            call_record_obj = CallRecord(
                user, other_user, direction, duration, timestamp, cell_id, cost, index=i)
            call_records.append(call_record_obj)
        fieldnames_ = ['user', 'other_user', 'direction', 'duration', 'timestamp', 'call_id', 'cost']
        filtered_call_records, bad_records = parse_records(call_records, fieldnames_)
        call_dataset_obj = CallDataSet(filtered_call_records, fieldnames_)

        print("[x]  Dataset object creation successful\n")
        return call_dataset_obj


def create_msg_obj(messages, fieldnames, hash):
    if type(messages) != list or type(hash) != bool:
        raise TypeError
    elif messages is not None:

        msg_records = []
        for msg in messages:
            user = other_user = direction = length = timestamp = None

            for key in msg:
                if not isinstance(msg[key], str):
                    msg[key] = str(msg[key])
                if 'user' in key:
                    if hash and msg['user'] != '':
                        user = hash_number(msg[key])
                    else:
                        user = msg[key]
                elif 'other' in key:
                    if hash and msg['other'] != '':
                        other_user = hash_number(msg[key])
                    else:
                        other_user = msg[key]
                elif 'dir' in key:
                    direction = msg[key]
                elif 'len' in key:
                    length = msg[key]
                elif 'time' in key:
                    timestamp = msg[key]

            message_record_obj = MessageRecord(
                user, other_user, direction, length, timestamp)
            msg_records.append(message_record_obj)
        filtered_message_records, bad_records = parse_records(msg_records, fieldnames)
        message_dataset_obj = MessageDataSet(filtered_message_records, fieldnames)

        print("[x]  Dataset object creation successful\n")
        return message_dataset_obj


def create_cell_obj(cells, fieldnames, call_data_set):
    if type(cells) != list:
        raise TypeError
    elif type(call_data_set).__name__ != "CallDataSet" and call_data_set is not None:
        raise TypeError
    elif cells is not None:
        cell_records = []
        for cell in cells:
            cell_id = latitude = longitude = None

            for key in cell:
                if not isinstance(cell[key], str):
                    cell[key] = str(cell[key])
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
        print("[x]  Dataset object creation successful\n")
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
