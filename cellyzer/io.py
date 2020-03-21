"""
Methods
---------
reading,writing datasets in many file types (csv,xlsx,txt)
altering datasets (removing columns etc.)

"""


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


def read_msg():
    print("[x]  Reading Message Data")
    read_csv()

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
