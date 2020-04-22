import unittest
import cellyzer.core as core
import cellyzer.io as io


class TestCallMessageDataSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # before all the tests
        cls.user1 = "7163185791"
        cls.user2 = "7187432175"
        cls.user3 = '7641036117'

        cls.callDataSet = core.CallDataSet()
        call_file_path = "../../dataset/my_test_data/calls.csv"
        cls.callDataSet = io.read_call(call_file_path)

        cls.msgDataSet = core.MessageDataSet()
        msg_file_path = "../../dataset/my_test_data/messages.csv"
        cls.msgDataSet = io.read_msg(msg_file_path)

    @classmethod
    def tearDownClass(cls):
        # after all the tests
        pass

    def setUp(self):
        # run before each test
        pass

    def tearDown(self):
        # run after each test
        pass

    # functions

    def test_get_records(self):
        print("test - get records")

    def test_get_all_users(self):
        print("test - get all users")

    def test_get_connected_users(self):
        print("test - get connected users")

    def test_connection_matrix(self):
        print("test - connection matrix")

    def test_get_connections(self):
        print("test - get connections")


if __name__ == '__main__':
    unittest.main()
