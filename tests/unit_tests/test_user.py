import unittest
import cellyzer.core as core
import cellyzer.io as io


class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # before all the tests
        cls.user1_contact_no = "3e97992791"
        cls.user2_contact_no = "8d27cf2694"
        cls.user3_contact_no = '329233d117'

        cls.callDataSet = core.CallDataSet()
        call_file_path = "../../demo/demo_datasets/test_data/calls.csv"
        cls.callDataSet = io.read_call(call_file_path)

        cell_file_path = "../../demo/demo_datasets/test_data/antennas.csv"
        # cls.cellDataSet = core.CellDataSet( )
        cls.cellDataSet = io.read_cell(cell_file_path, call_dataset_obj=cls.callDataSet)

        cls.user1 = core.User(callDataSet=cls.callDataSet, cellDataSet=cls.cellDataSet, contact_no=cls.user1_contact_no)
        cls.user2 = core.User(callDataSet=cls.callDataSet, cellDataSet=cls.cellDataSet, contact_no=cls.user2_contact_no)
        cls.user3 = core.User(callDataSet=cls.callDataSet, cellDataSet=cls.cellDataSet, contact_no=cls.user3_contact_no)
        cls.user3_new = core.User(callDataSet=cls.callDataSet, cellDataSet=cls.cellDataSet,
                                  contact_no=cls.user3_contact_no, work_start_time=15, work_end_time=22)

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
        self.assertEqual(self.user1.get_contact_no(), self.user1_contact_no)
        self.assertEqual(self.user2.get_contact_no(), self.user2_contact_no)
        self.assertEqual(type(self.user2.get_contact_no()), str)

    def test_compute_home(self):
        self.assertEqual(self.user1.compute_home(), [42.304917, -71.147374])
        self.assertEqual(self.user2.compute_home(), [42.386722, -71.138778])
        self.assertEqual(self.user3.compute_home(), [42.304917, -71.147374])
        self.assertEqual(self.user3_new.compute_home(), [42.304917, -71.147374])

    def test_compute_work_location(self):
        self.assertEqual(self.user1.compute_work_location(), [42.386722, -71.138778])
        self.assertEqual(self.user2.compute_work_location(), [42.386722, -71.138778])
        self.assertEqual(self.user3.compute_work_location(), [42.3604, -71.087374])
        self.assertEqual(self.user3_new.compute_work_location(), [42.345, -71.09])

    def test_check_timestamp_for_home(self):
        user1_records = self.callDataSet.get_records(self.user1_contact_no)
        self.assertEqual(self.user1.check_timestamp_for_home(user1_records[0]), True)
        self.assertEqual(self.user1.check_timestamp_for_home(user1_records[1]), False)
        self.assertEqual(self.user1.check_timestamp_for_home(user1_records[2]), False)

    def test_get_home_location(self):
        self.assertEqual(self.user1.get_home_location(), [42.304917, -71.147374])
        self.assertEqual(self.user2.get_home_location(), [42.386722, -71.138778])
        self.assertEqual(self.user3.get_home_location(), [42.304917, -71.147374])
        self.assertEqual(self.user3_new.get_home_location(), [42.304917, -71.147374])

    def test_get_work_location(self):
        self.assertEqual(self.user1.get_work_location(), [42.386722, -71.138778])
        self.assertEqual(self.user2.get_work_location(), [42.386722, -71.138778])
        self.assertEqual(self.user3.get_work_location(), [42.3604, -71.087374])
        self.assertEqual(self.user3_new.get_work_location(), [42.345, -71.09])

    def test_get_home_location_related_cell_id(self):
        self.assertEqual(self.user1.get_home_location_related_cell_id(), "10")
        self.assertEqual(self.user2.get_home_location_related_cell_id(), "2")
        self.assertEqual(self.user3.get_home_location_related_cell_id(), "10")
        self.assertEqual(self.user3_new.get_home_location_related_cell_id(), "10")

    def test_get_work_location_related_cell_id(self):
        self.assertEqual(self.user1.get_work_location_related_cell_id(), "2")
        self.assertEqual(self.user2.get_work_location_related_cell_id(), "2")
        self.assertEqual(self.user3.get_work_location_related_cell_id(), "3")
        self.assertEqual(self.user3_new.get_work_location_related_cell_id(), "7")

    def test_get_ignored_call_details(self):
        self.assertEqual(self.user1.get_ignored_call_details(), [])

        user3_result = [{'other user': '0041628436', 'date': '11-02-1980', 'time stamp': '08:06:18', 'cell ID': '5'}]
        self.assertEqual(self.user3.get_ignored_call_details(), user3_result)


if __name__ == '__main__':
    unittest.main()
