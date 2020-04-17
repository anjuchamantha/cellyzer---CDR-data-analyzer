"""
This is for manual testing the library
"""

import cellyzer as cz

call_file_path = "dataset/my_test_data/calls.csv"
antenna_file_path = "dataset/my_test_data/antennas.csv"
callDataSet = cz.read_call(call_file_path)

antennaDataSet = cz.read_cell(antenna_file_path, call_dataset_obj=callDataSet, file_type='csv')
# record = antennaDataSet.get_cell_records(cell_id=1)
# print("cell id - ", record.get_cell_id())


population = antennaDataSet.get_population()
print(">> population around cell")
print(population)
cz.utils.tabulate_list_of_dictionaries(population)
cz.visualization.cell_population_visualization(population)

# call_made_locations = antennaDataSet.get_trip_details("7110730864", console_print=True, tabulate=True)
# cz.visualization.trip_visualization(call_made_locations)

