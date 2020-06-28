from collections import OrderedDict

import tabulate


def print_record_lists(records):
    for record in records:
        print(vars(record))


def print_dataset(dataset_obj, notebook=False, name="Dataset", rows=None, summerize=False, head=5, tail=5):
    if rows is not None:
        if rows > 50:
            summerize = True

    # print a demo_datasets obj as a dictionary
    print("\n >>> %s :" % name)
    dict_list = []
    records = dataset_obj.get_records()
    len_records = len(records)
    if len_records > 50:
        summerize = True
    if summerize:
        for record in records[:head]:
            dict_list.append(record.__dict__)
        dict_list.append({})
        for record in records[-tail:]:
            dict_list.append(record.__dict__)
    else:
        for record in records:
            dict_list.append(record.__dict__)
    header = list(dict_list[0].keys())
    rows = []
    for i in range(0, len(dict_list)):
        values = list(dict_list[i].values())
        rows.append(values)
    if notebook:
        print(tabulate.tabulate(rows, header, tablefmt='html'))
    else:
        print(tabulate.tabulate(rows, header, tablefmt='pretty'))
    return [header, dict_list]


def print_close_contacts(close_contact_dict):
    # print close contacts as a dictionary
    header = ["contact no", "no of interactions between users"]
    rows = []
    for key, value in close_contact_dict.items():
        row = [key, value]
        rows.append(row)
    print(tabulate.tabulate(rows, header, tablefmt='pretty'))


def tabulate_list_of_dictionaries(dictionary_list):
    """
    tabulate the list of dictionaries

    :param dictionary_list: list

    :return: print table
    """
    if not dictionary_list:
        return None
    if type(dictionary_list) == list:
        header = []
        for item in dictionary_list[0].keys():
            header.append(item)
        rows = []
        for cell in dictionary_list:
            row = []
            for key in cell.keys():
                row.append(cell[key])
            rows.append(row)

        print(tabulate.tabulate(rows, header, tablefmt='pretty'))


def flatten(d, parent_key='', separator='__'):
    """
    Flatten a nested dictionary.

    Parameters
    ----------
    d: dict_like
        Dictionary to flatten.
    parent_key: string, optional
        Concatenated names of the parent keys.
    separator: string, optional
        Separator between the names of the each key.
        The default separator is '_'.

    """
    items = []
    for k, v in d.items():
        new_key = parent_key + separator + k if parent_key else k
        if isinstance(v, (dict, OrderedDict)):
            items.extend(flatten(v, new_key, separator).items())
        else:
            items.append((new_key, v))
    return OrderedDict(items)
