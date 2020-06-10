import cProfile
import cellyzer.io as io

call_file_path = "../../demo/demo_datasets/long_data/calls_.csv"
msg_file_path = "../../demo/demo_datasets/long_data/messages_.csv"
cell_file_path = "../../demo/demo_datasets/long_data/antennas.csv"


def test_read_call():
    io.read_call(call_file_path)


def test_read_msg():
    io.read_msg(msg_file_path)


def test_read_cell():
    io.read_cell(cell_file_path, call_dataset_obj=io.read_call(call_file_path))


# cProfile run functions
cProfile.run('test_read_call()')
cProfile.run('test_read_msg()')
cProfile.run('test_read_cell()')
