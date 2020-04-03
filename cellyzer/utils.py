def print_dataset_dict(dataset_obj):
    # print a dataset obj as a dictionary
    for record in dataset_obj.get_records():
        print(vars(record))
