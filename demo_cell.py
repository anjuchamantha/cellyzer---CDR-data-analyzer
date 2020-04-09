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

pop = antennaDataSet.get_population(callDataSet)
print(pop)

cz.utils.print_population_around_cell(pop)

# cz.visualization.cell_population_visualization(pop)
