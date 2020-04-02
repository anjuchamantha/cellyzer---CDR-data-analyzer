"""
This is for manual testing the library
"""

import cellyzer as cz

# cz.read_call("csv")
# cz.utils.utils_func()


# cz.core.graph()



msg_file_path = "../dataset/my_test_data/messages.csv"
cz.read_msg(msg_file_path)

# call_file_path = "../dataset/my_test_data/call.csv"
# cz.read_call(call_file_path)