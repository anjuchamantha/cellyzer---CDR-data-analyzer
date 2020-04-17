"""
This is for manual testing the library
"""

import cellyzer as cz

call_file_path = "G:\data\excel\calls.xlsx"
antenna_file_path = "G:\data\excel\cell.xlsx"
callDataSet = cz.read_call(call_file_path, 'xlsx')

antennaDataSet = cz.read_cell(antenna_file_path, call_dataset_obj=callDataSet, file_type='xlsx')
# record = antennaDataSet.get_cell_records(cell_id=1)
# print("cell id - ", record.get_cell_id())

# all_records = antennaDataSet.get_cell_records()
# for i in all_records:
#     print('demo class all records : ', i.get_cell_id())

population = antennaDataSet.get_population()
print(population)

cz.utils.tabulate_list_of_dictionaries(population)

# filepath_to_save = "D:\SE Project sem5"
filepath_to_save = "F:/SEMESTER 5/CS3202 - SE Project/maps/"
# cz.visualization.cell_population_visualization(population, filepath_to_save)

# population = antennaDataSet.get_population()
# print(population)

# filepath_to_save = "D:\SE Project sem5"
# cz.visualization.cell_population_visualization(population, filepath_to_save)
#
call_made_locations = antennaDataSet.get_trip_details("7110730864", console_print=True, tabulate=True)
cz.visualization.trip_visualization(call_made_locations)
