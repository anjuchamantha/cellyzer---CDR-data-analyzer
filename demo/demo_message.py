import cellyzer as cz

msg_file_path = "demo_datasets/test_data/messages.csv"
messageDataSet = cz.read_msg(msg_file_path)

# Print the data set
# cz.utils.print_dataset(messageDataSet, name="Message Dataset")

# Get all the users in the data set
# all_users = messageDataSet.get_all_users()
# print("All Users : %s \n" % all_users)
#
search_user1 = "0041628436"
search_user2 = "329233d117"

# Get all the users connected to given user
# connected_users = messageDataSet.get_connected_users("329233d117")
# print("Users connected to %s : %s \n" % (search_user1, connected_users))

# Get all the records of the given user/2 users
user_record_list = messageDataSet.get_records(search_user1, search_user2)
# cz.utils.print_record_lists(user_record_list)

# make a new data set object with selected record objects from user records of the given 2 users
user_message_dataset = cz.MessageDataSet(user_record_list)
cz.utils.print_dataset(user_message_dataset, name="New Message DataSet obj : User Records of %s" % search_user1 + " & " + search_user2)
#save dataset as a csv file
cz.io.to_json(user_message_dataset,"records_of_2_users")
# create a date time object with a timestamp string
# date = cz.tools.get_datetime_from_timestamp("Mon Feb 11 07:08:49 +0000 1980")

# print a connection matrix of all the users
# messageDataSet.print_connection_matrix()

# visualize the connections with the directions and number of connections
# messageDataSet.visualize_connection_network()

# top 3 close contacts of a given user
# close_contacts = messageDataSet.get_close_contacts(search_user2, top_contact=3)
# print(">> close contacts of %s :" % search_user1)
# cz.utils.print_close_contacts(close_contacts)
#
# msg_connections = messageDataSet.get_connections()
# print(">> All the connections %s :" % msg_connections)
# print(msg_connections)
