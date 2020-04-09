"""
This is for manual testing the library
"""

import cellyzer as cz

call_file_path = "dataset/my_test_data/calls.csv"
callDataSet = cz.read_call(call_file_path)

antenna_file_path = "dataset/my_test_data/antennas.csv"
antennaDataSet = cz.read_cell(antenna_file_path)

# record = antennaDataSet.get_cell_records(cell_id=1)
# print("cell id - ", record.get_cell_id())

# all_records = antennaDataSet.get_cell_records()
# for i in all_records:
#     print('demo class all records : ', i.get_cell_id())

population = antennaDataSet.get_population(callDataSet)
print(population)

cz.utils.print_population_around_cell(population)

filepath_to_save = "F:/SEMESTER 5/CS3202 - SE Project/maps/"
cz.visualization.cell_population_visualization(population, filepath_to_save)
