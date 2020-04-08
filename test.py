import cellyzer as cz

call_file_path = "dataset/my_test_data/antennas.csv"
callDataSet = cz.read_csv(call_file_path)

cz.to_json(callDataSet, 'ABC')

