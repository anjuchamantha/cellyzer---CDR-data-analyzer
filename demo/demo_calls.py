"""
This is for manual testing the library
"""

import cellyzer as cz

call_file_path = "demo_datasets/long_data/calls_.csv"
callDataSet = cz.read_call(call_file_path)
cz.utils.print_dataset(callDataSet, name="Call Dataset")

all_users_of_calls = callDataSet.get_all_users()
print("All Users in call dataSet : %s \n" % all_users_of_calls)

search_user_call_1 = "3e97992791"
search_user_call_2 = "265034e175"
search_user_call_3 = '329233d117'

connected_users_calls = callDataSet.get_connected_users(search_user_call_1)
print("Users connected to %s : %s \n" % (search_user_call_1, connected_users_calls))

user_call_record_list = callDataSet.get_records(search_user_call_1, search_user_call_2)
print(">> call records between %s and %s" % (search_user_call_1, search_user_call_2))
cz.utils.print_record_lists(user_call_record_list)

user_call_dataset = cz.MessageDataSet(user_call_record_list)
cz.utils.print_dataset(user_call_dataset, name="User Records of %s" % search_user_call_1 + " " + search_user_call_2)

print(">> connection matrix")
callDataSet.print_connection_matrix()
# print(a)
# print(b)

callDataSet.visualize_connection_network()

close_contacts = callDataSet.get_close_contacts(search_user_call_3, top_contact=4)
print(">> close contacts of %s : %s" % (search_user_call_1, close_contacts))
cz.utils.print_close_contacts(close_contacts)

active_time = callDataSet.get_most_active_time(search_user_call_1)
print(">> most active times during day of %s - %s" % (search_user_call_1, active_time))
cz.visualization.active_time_bar_chart(active_time)

ignored_call_details = callDataSet.get_ignored_call_details(search_user_call_3)
print(">> ignored calls details : ")
print(ignored_call_details)
cz.utils.tabulate_list_of_dictionaries(ignored_call_details)

call_records_around_cell = callDataSet.get_call_records_by_antenna_id(cell_id='1')
print("number of call records around cell_id - %s = %s" % (1, len(call_records_around_cell)))

call_connections = callDataSet.get_connections()
print(call_connections)