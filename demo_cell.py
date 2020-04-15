"""
This is for manual testing the library
"""

import cellyzer as cz

call_file_path = "dataset/my_test_data/calls.csv"
antenna_file_path = "dataset/my_test_data/antennas.csv"
callDataSet = cz.read_call(call_file_path)

antennaDataSet = cz.read_cell(antenna_file_path, call_dataset_obj=callDataSet)

# population = antennaDataSet.get_population()
# print(population)
#
# cz.utils.print_population_around_cell(population)
#
# filepath_to_save = "D:\SE Project sem5"
# cz.visualization.cell_population_visualization(population, filepath_to_save)

call_made_locations = antennaDataSet.get_trip_details("7110730864", console_print=True, tabulate=True)
cz.visualization.trip_visualization(call_made_locations)
