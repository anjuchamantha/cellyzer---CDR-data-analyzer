"""
This is for manual testing the library
"""

import cellyzer as cz

call_file_path = "demo_datasets/long_data/calls_.csv"
antenna_file_path = "demo_datasets/test_data/antennas.csv"
callDataSet = cz.read_call(call_file_path)
cz.read_cell(antenna_file_path, call_csv_path=None)
antennaDataSet = cz.read_cell(antenna_file_path, call_dataset_obj=callDataSet, file_type='csv')

# print antenna data set
# cz.utils.print_dataset(antennaDataSet, name="Antenna Data set")

# get a record of a given cell id
# record = antennaDataSet.get_cell_records(cell_id=1)
# print("Record of cell %s : %s \n" % (1, record.__dict__))
#
# print(">> population around cell")
# population = antennaDataSet.get_population()
# print(population)
# cz.utils.tabulate_list_of_dictionaries(population)
# cz.visualization.cell_population_visualization(population)
#
# print(">> Trip details of user : %s" % "8d27cf2694")
# call_made_locations = antennaDataSet.get_trip_details("8d27cf2694", console_print=True, tabulate=True)
# cz.visualization.trip_visualization(call_made_locations, notebook=False)
#
# test = callDataSet.get_records()
# print(">> Unique users")
# print(antennaDataSet.get_unique_users_around_cell(test))
#
# print(">> Is %s recorded in cell %s" % ("123", 10))
# print(antennaDataSet.check_user_location_matches_cell(contact_no='123', cell_id=10))
