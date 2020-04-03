"""
Methods
---------
reading,writing datasets in many file types (csv,xlsx,txt)
altering datasets (removing columns etc.)

"""

import csv
from .core import DataSet, MessageDataSet, CallDataSet, Record, CallRecord, MessageRecord, CellRecord


def io_func():
    print("I am from io")
    return


def read_csv():
    print("         from a CSV file ...")

    """
     Load records from a csv file.

    Parameters
    ----------
    path : str
        Path of the file.

    """
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

            create_call_obj(call_list)
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

            # for m in messages_list:
            #     print(m)
            # messages = dict((d['user'], ( d['other'], d['direction'], d['length'], d['timestamp'] )) for d in reader)

            return create_msg_obj(messages_list,fieldnames)
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
    pass


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


def create_call_obj(calls):
    if calls is not None:
        call_dataset_obj = CallDataSet()


def create_msg_obj(messages,fieldnames):
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
        message_dataset_obj = MessageDataSet(msg_records,fieldnames)

        # print("[x]  Objects creation successful\n")
        return message_dataset_obj
