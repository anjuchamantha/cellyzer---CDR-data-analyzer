"""
This is for manual testing the library
"""

import cellyzer as cz

# cz.read_call("csv")
# cz.utils.utils_func()


# cz.core.graph()


msg_file_path = "dataset/my_test_data/messages.csv"
messageDataSet = cz.read_msg(msg_file_path)
# cz.utils.print_dataset(messageDataSet, name="Message Dataset")

# all_users = messageDataSet.get_all_users()
# print("All Users : %s \n" % all_users)

# search_user1 = "7681546436"
# search_user2 = "7641036117"

# connected_users = messageDataSet.get_connected_users(search_user1)
# print("Users connected to %s : %s \n" % (search_user1, connected_users))

# user_record_list = messageDataSet.get_records(search_user1, search_user2)
# cz.utils.print_record_lists(user_record_list)

# user_message_dataset = cz.MessageDataSet(user_record_list)
# cz.utils.print_dataset(user_message_dataset, name="User Records of %s" % search_user1 + " " + search_user2)

# date = cz.tools.get_date_from_timestamp("Mon Feb 11 07:08:49 +0000 1980")
# print(date)
#
# messageDataSet.print_connection_matrix()
#
# messageDataSet.visualize_connection_network()

# ---------------------call functions demo---------------

call_file_path = "dataset/my_test_data/calls.csv"
callDataSet = cz.read_call(call_file_path)

all_users_of_calls = callDataSet.get_all_users()
# print("All Users in call dataSet : %s \n" % all_users_of_calls)

search_user_call_1 = "7981267897"
search_user_call_2 = "7743039441"

connected_users_calls = callDataSet.get_connected_users(search_user_call_1)
print("Users connected to %s : %s \n" % (search_user_call_1, connected_users_calls))

user_call_record_list = callDataSet.get_records(search_user_call_1, search_user_call_2)
print(">> call records between %s and %s" % (search_user_call_1, search_user_call_2))
cz.utils.print_record_lists(user_call_record_list)

user_call_dataset = cz.MessageDataSet(user_call_record_list)
cz.utils.print_dataset(user_call_dataset, name="User Records of %s" % search_user_call_1 + " " + search_user_call_2)

callDataSet.print_connection_matrix()

# callDataSet.visualize_connection_network()

close_contacts = callDataSet.get_close_contacts(search_user_call_1, top_contact=2)
print(">> close contacts of %s : %s" % (search_user_call_1, close_contacts))
cz.utils.print_close_contacts(close_contacts)

