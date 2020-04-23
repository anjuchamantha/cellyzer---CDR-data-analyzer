"""
This is for manual testing the library
"""

import cellyzer as cz

call_file_path = "demo_datasets/test_data/calls.csv"
# message_file_path = "demo_datasets/test_data/messages.csv"
antenna_file_path = "demo_datasets/test_data/antennas.csv"

callDataSet = cz.read_call(call_file_path)
# messageDataSet = cz.read_msg(message_file_path)
cellDataSet = cz.read_cell(antenna_file_path)

user_number = "3e97992791"
user2_number = "8d27cf2694"
# date = cz.tools.get_date_from_timestamp("Mon Feb 11 07:08:49 +0000 1980")
# print(date)

user1 = cz.User(callDataSet=callDataSet, cellDataSet=cellDataSet, contact_no=user_number)
user2 = cz.User(callDataSet=callDataSet, cellDataSet=cellDataSet, contact_no=user2_number)
# filepath_to_save = "F:/SEMESTER 5/CS3202 - SE Project/maps/"

location_home = user1.get_home_location()
print('>> home location : ', location_home)
home_cell_id = user1.get_home_location_related_cell_id()
print(">> home location -> cell id : ", home_cell_id)

location_office = user1.get_work_location()
print('>> work location : ', location_office)
officeplace_cell_id = user1.get_work_location_related_cell_id()
print(">> work location -> cell id : ", officeplace_cell_id)

cz.visualization.view_home_work_locations(home_location=location_home, work_location=location_office)

user3_number = '329233d117'
user3 = cz.User(callDataSet=callDataSet, cellDataSet=cellDataSet, contact_no=user3_number, work_start_time=15,
                work_end_time=22)
ignored_call_details = user3.get_ignored_call_details()
print(">> ignored calls details : ")
print(ignored_call_details)
cz.utils.tabulate_list_of_dictionaries(ignored_call_details)


location_home = user3.get_home_location()
print('>> home location : ', location_home)
home_cell_id = user3.get_home_location_related_cell_id()
print(">> home location -> cell id : ", home_cell_id)

location_office = user3.get_work_location()
print('>> work location : ', location_office)
officeplace_cell_id = user3.get_work_location_related_cell_id()
print(">> work location -> cell id : ", officeplace_cell_id)
