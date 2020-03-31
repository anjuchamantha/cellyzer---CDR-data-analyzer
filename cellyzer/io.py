"""
Methods
---------
reading,writing datasets in many file types (csv,xlsx,txt)
altering datasets (removing columns etc.)

"""

import csv

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


def read_call(type):
    print("[x]  Reading Call Data")
    if type=="csv":
        read_csv()

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
    print("[x]  Reading Message Data")

    try:
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            messages = dict((d['user'], ( d['other'], d['direction'], d['length'], d['timestamp'] )) for d in reader)

    except IOError:
        pass


    for key in messages:
        print(key , messages[key])

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
