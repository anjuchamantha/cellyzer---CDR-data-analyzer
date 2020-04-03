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
