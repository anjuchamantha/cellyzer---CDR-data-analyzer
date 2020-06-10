import cProfile
import cellyzer.io as io
import cellyzer.core as core

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

cell_file_path = "../../demo/demo_datasets/long_data/antennas.csv"
cellDataSet = io.read_cell(cell_file_path, call_dataset_obj=callDataSet)

user1_obj = core.User(callDataSet=callDataSet, cellDataSet=cellDataSet, contact_no=user1)
user2_obj = core.User(callDataSet=callDataSet, cellDataSet=cellDataSet, contact_no=user2)
user3_obj = core.User(callDataSet=callDataSet, cellDataSet=cellDataSet, contact_no=user3)


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
def test_get_contact_no():
    user1_obj.get_contact_no()


def test_compute_home():
    user1_obj.compute_home()


def test_compute_work_location():
    user1_obj.compute_work_location()


def test_check_timestamp_for_home():
    user1_records = callDataSet.get_records(user1)
    user1_obj.check_timestamp_for_home(user1_records[0])


def test_get_home_location():
    user1_obj.get_home_location()


def test_get_work_location():
    user1_obj.get_work_location()


def test_get_home_location_related_cell_id():
    user1_obj.get_home_location_related_cell_id()


def test_get_work_location_related_cell_id():
    user1_obj.get_work_location_related_cell_id()


def test_user_get_ignored_call_details():
    user1_obj.get_ignored_call_details()


# ################################################################  cProfile run
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

cProfile.run('test_get_contact_no()')
cProfile.run('test_compute_home()')
cProfile.run('test_compute_work_location()')
cProfile.run('test_check_timestamp_for_home()')
cProfile.run('test_get_home_location()')
cProfile.run('test_get_work_location()')
cProfile.run('test_get_home_location_related_cell_id()')
cProfile.run('test_get_work_location_related_cell_id()')
cProfile.run('test_get_ignored_call_details()')
