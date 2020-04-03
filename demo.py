"""
This is for manual testing the library
"""

import cellyzer as cz
import pprint

# cz.read_call("csv")
# cz.utils.utils_func()


# cz.core.graph()


msg_file_path = "../dataset/my_test_data/messages.csv"
messageDataSet = cz.read_msg(msg_file_path)

all_users = messageDataSet.get_all_users()
print("All Users : %s \n" % all_users)

connected_users = messageDataSet.get_connected_users("7610039694")
print("Users connected to 7610039694 : %s \n" % connected_users)

user_record_list = messageDataSet.get_records("7610039694")
user_message_dataset = cz.MessageDataSet(user_record_list)
cz.utils.print_dataset_dict(user_message_dataset)

# call_file_path = "../dataset/my_test_data/call.csv"
# cz.read_call(call_file_path)
