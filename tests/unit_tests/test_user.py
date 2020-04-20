import unittest
import cellyzer.core as core
import cellyzer.io as io


class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # before all the tests
        cls.user1_contact_no = "7163185791"

        cls.callDataSet = core.CallDataSet()
        call_file_path = "../../dataset/my_test_data/calls.csv"
        cls.callDataSet = io.read_call(call_file_path)

        cell_file_path = "../../dataset/my_test_data/antennas.csv"
        # cls.cellDataSet = core.CellDataSet( )
        cls.cellDataSet = io.read_cell(cell_file_path, call_dataset_obj=cls.callDataSet)

        cls.user1 = core.User(callDataSet=cls.callDataSet, cellDataSet=cls.cellDataSet, contact_no=cls.user1_contact_no)

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

    def test_get_contact_no(self):
        print("test - get contact no")

    def test_get_user_calldata(self):
        print('test - get_user_calldata')

    def test_compute_home(self):
        print('test - compute home')


if __name__ == '__main__':
    unittest.main()
