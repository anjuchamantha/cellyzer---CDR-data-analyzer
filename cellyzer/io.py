"""
Methods
---------
reading,writing datasets in many file types (csv,xlsx,txt)
altering datasets (removing columns etc.)

"""

import csv
from .core import DataSet, MessageDataSet, CallDataSet, CellDataSet, Record, CallRecord, MessageRecord, CellRecord


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


def read_call(call_file_path):
    # print("[x]  Reading Call Data")

    try:
        with open(call_file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)

            fieldnames = reader.fieldnames
            call_list = []
            for val in reader:
                call = dict()
                for f in fieldnames:
                    call[f] = val[f]
                call_list.append(call)
            return create_call_obj(call_list, fieldnames)
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


def read_cell(file_path, call_csv_path=None, call_dataset_obj=None):
    try:
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
    except IOError:
        print('IO Error :', IOError)
        pass
    """
     Load cell records from a file.

    Parameters
    ----------
    path : str
        Path of the file.

    type : str
        Type of the file. (CSV,xls,json etc)


    """


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
            user = other_user = direction = duration = timestamp = cell_id = cost = None

            for key in call:
                if 'user' in key:
                    user = call["user"]
                elif 'other' in key:
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
        call_dataset_obj = CallDataSet(call_records, fieldnames)

        # print("[x]  Objects creation successful\n")
        return call_dataset_obj


def create_msg_obj(messages, fieldnames):
    if messages is not None:

        msg_records = []
        for msg in messages:
            user = other_user = direction = length = timestamp = None

            for key in msg:
                if 'user' in key:
                    user = msg[key]
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
        cell_dataset_obj = CellDataSet(cell_records, fieldnames, call_data_set)

        return cell_dataset_obj
