import cProfile
import cellyzer.io as io

# setup
user1 = "8d27cf2694"
user2 = "373a4fb419"
user3 = '329233d117'
user4 = "d235863694"
user5 = "e59cd92671"

call_file_path = "../../demo/demo_datasets/long_data/calls_.csv"
callDataSet = io.read_call(call_file_path)

msg_file_path = "../../demo/demo_datasets/long_data/messages_.csv"
msgDataSet = io.read_msg(msg_file_path)

cell_file_path = "../../demo/demo_datasets/test_data/antennas.csv"
cellDataSet = io.read_cell(cell_file_path, call_dataset_obj=callDataSet)


# 8d27cf2694
# 373a4fb419
# 329233d117
# 6cfc4bd054
# e98994c239
# 0041628436

# d235863694
# e59cd92671
# 07f0750117
# 4b1c2de436
# 9bf7b67897
# 25efbc7582
# 9ac45dd266
# 18423b0678

# ############################# callMessage Data set functions
def test_get_records():
    callDataSet.get_records()


def test_get_all_users():
    callDataSet.get_all_users()


def test_get_connected_users():
    callDataSet.get_connected_users(user1)


def test_get_connections():
    callDataSet.get_connections(allow_duplicates=True)


# ##############################  call Data set Functions
def test_get_most_active_time():
    callDataSet.get_most_active_time(user=user1)


def test_get_close_contacts():
    callDataSet.get_close_contacts(user=user1, top_contact=2)


def test_get_call_records_by_antenna_id():
    callDataSet.get_call_records_by_antenna_id(cell_id=1)


def test_get_ignored_call_details():
    callDataSet.get_ignored_call_details(user=user1)


# ###################################  Message Data set functions
def test_msg_get_close_contacts():
    msgDataSet.get_close_contacts(user=user4, top_contact=2)


# ##################################   Cell data set functions
def test_get_cell_records():
    cellDataSet.get_cell_records()


def test_get_location():
    cellDataSet.get_location(1)


def test_get_population():
    cellDataSet.get_population()


def test_get_unique_users_around_cell():
    cellDataSet.get_unique_users_around_cell(callDataSet.get_records())


def test_check_user_location_matches_cell():
    cellDataSet.check_user_location_matches_cell(user1, 2)


def test_get_trip_details():
    cellDataSet.get_trip_details(user1)


# ##################################  User functions

#################################################################
cProfile.run('test_get_records()')
cProfile.run('test_get_all_users()')
cProfile.run('test_get_connected_users()')
cProfile.run('test_get_connections()')

cProfile.run('test_get_most_active_time()')
cProfile.run('test_get_close_contacts()')
cProfile.run('test_get_call_records_by_antenna_id()')
cProfile.run('test_get_ignored_call_details()')

cProfile.run('test_msg_get_close_contacts()')

cProfile.run('test_get_cell_records()')
cProfile.run('test_get_location()')
cProfile.run('test_get_population()')
cProfile.run('test_get_unique_users_around_cell()')
cProfile.run('test_check_user_location_matches_cell()')
cProfile.run('test_get_trip_details()')
