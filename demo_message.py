import cellyzer as cz

msg_file_path = "dataset/my_test_data/messages.csv"
messageDataSet = cz.read_msg(msg_file_path)
cz.utils.print_dataset(messageDataSet, name="Message Dataset")

# all_users = messageDataSet.get_all_users()
# print("All Users : %s \n" % all_users)
#
# search_user1 = "7681546436"
# search_user2 = "7641036117"
#
# connected_users = messageDataSet.get_connected_users(search_user1)
# print("Users connected to %s : %s \n" % (search_user1, connected_users))
#
# user_record_list = messageDataSet.get_records(search_user1, search_user2)
# cz.utils.print_record_lists(user_record_list)
#
# user_message_dataset = cz.MessageDataSet(user_record_list)
# cz.utils.print_dataset(user_message_dataset, name="User Records of %s" % search_user1 + " & " + search_user2)
#
# date = cz.tools.get_datetime_from_timestamp("Mon Feb 11 07:08:49 +0000 1980")
# print(date)
#
# messageDataSet.print_connection_matrix()
#
# messageDataSet.visualize_connection_network()
