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
for msgRecord in messageDataSet.get_records():
    print(vars(msgRecord))

# call_file_path = "../dataset/my_test_data/call.csv"
# cz.read_call(call_file_path)
