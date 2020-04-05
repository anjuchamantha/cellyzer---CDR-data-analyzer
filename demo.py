"""
This is for manual testing the library
"""

import cellyzer as cz

# reading message dataset and creating a message dataset object
msg_file_path = "dataset/my_test_data/messages.csv"
messageDataSet = cz.read_msg(msg_file_path)
# cz.utils.print_dataset(messageDataSet, name="Message Dataset")

# get all the users in the dataset
all_users = messageDataSet.get_all_users()
print("All Users : %s \n" % all_users)

# getting a list of users who are connected to a given user
search_user1 = "7681546436"
search_user2 = "7641036117"
connected_users = messageDataSet.get_connected_users(search_user1)
print("Users connected to %s : %s \n" % (search_user1, connected_users))

# getting the records of given 2 users
user_record_list = messageDataSet.get_records(search_user1, search_user2)
# cz.utils.print_record_lists(user_record_list)

# creating a new message dataset object with only those given 2 users
user_message_dataset = cz.MessageDataSet(user_record_list)
cz.utils.print_dataset(user_message_dataset, name="User Records of %s" % search_user1 + " " + search_user2)

# getting date object from timestamp
date = cz.tools.get_date_from_timestamp("Mon Feb 11 07:08:49 +0000 1980")
print(date)

# printing a connection matrix of the message dataset
messageDataSet.print_connection_matrix()

# graph visualization of the connections in the dataset
messageDataSet.visualize_connection_network()
