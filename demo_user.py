"""
This is for manual testing the library
"""

import cellyzer as cz

call_file_path = "dataset/my_test_data/calls.csv"
# message_file_path = "dataset/my_test_data/messages.csv"
antenna_file_path = "dataset/my_test_data/antennas.csv"

callDataSet = cz.read_call(call_file_path)
# messageDataSet = cz.read_msg(message_file_path)
cellDataSet = cz.read_cell(antenna_file_path)

user_number = "7163185791"

# date = cz.tools.get_date_from_timestamp("Mon Feb 11 07:08:49 +0000 1980")
# print(date)

user1 = cz.User(callDataSet=callDataSet, cellDataSet=cellDataSet, contact_no=user_number)

filepath_to_save = "F:/SEMESTER 5/CS3202 - SE Project/maps/"

location_home = user1.get_home_location()
print('>> home location : ', location_home)
cz.visualization.view_home_location(location_home, filepath_to_save)

location_office = user1.get_work_location()
print('>> work location : ', location_office)
cz.visualization.view_work_location(location_office, filepath_to_save)
