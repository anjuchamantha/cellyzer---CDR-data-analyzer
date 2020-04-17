from collections import OrderedDict

import tabulate


def print_record_lists(records):
    for record in records:
        print(vars(record))


def print_dataset(dataset_obj, notebook=False, name="Dataset"):
    # print a dataset obj as a dictionary
    print("\n >>> %s :" % name)
    dict_list = []
    for record in dataset_obj.get_records():
        dict_list.append(vars(record))
    header = list(dict_list[0].keys())
    header.insert(0, '')
    # print (header)

    rows = []
    for i in range(0, len(dict_list)):
        values = list(dict_list[i].values())
        values.insert(0, i + 1)
        rows.append(values)
    # print (rows)
    if notebook:
        print(tabulate.tabulate(rows, header, tablefmt='html'))
    else:
        print(tabulate.tabulate(rows, header, tablefmt='pretty'))


def print_close_contacts(close_contact_dict):
    # print close contacts as a dictionary
    header = ["contact no", "no of calls between users"]
    rows = []
    for key, value in close_contact_dict.items():
        row = [key, value]
        rows.append(row)
    print(tabulate.tabulate(rows, header, tablefmt='pretty'))


def tabulate_list_of_dictionaries(population_dict):
    # print population as a table
    if type(population_dict) == list:
        header = []
        for item in population_dict[0].keys():
            header.append(item)
        rows = []
        for cell in population_dict:
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
