"""
This is for manual testing the library
"""

import cellyzer as cz

# ---------------------call functions demo---------------

call_file_path = "dataset/my_test_data/calls.csv"
callDataSet = cz.read_call(call_file_path)

all_users_of_calls = callDataSet.get_all_users()
# print("All Users in call dataSet : %s \n" % all_users_of_calls)

search_user_call_1 = "7163185791"
search_user_call_2 = "7187432175"

connected_users_calls = callDataSet.get_connected_users(search_user_call_1)
# print("Users connected to %s : %s \n" % (search_user_call_1, connected_users_calls))

user_call_record_list = callDataSet.get_records(search_user_call_1, search_user_call_2)
# print(">> call records between %s and %s" % (search_user_call_1, search_user_call_2))
# cz.utils.print_record_lists(user_call_record_list)

user_call_dataset = cz.MessageDataSet(user_call_record_list)
# cz.utils.print_dataset(user_call_dataset, name="User Records of %s" % search_user_call_1 + " " + search_user_call_2)

# callDataSet.print_connection_matrix()

# callDataSet.visualize_connection_network()

close_contacts = callDataSet.get_close_contacts(search_user_call_1, top_contact=2)
# print(">> close contacts of %s : %s" % (search_user_call_1, close_contacts))
# cz.utils.print_close_contacts(close_contacts)

active_time = callDataSet.get_most_active_time(search_user_call_1)
print(">> most active times during day of %s - %s"%(search_user_call_1,active_time))
cz.visualization.active_time_bar_chart(active_time)