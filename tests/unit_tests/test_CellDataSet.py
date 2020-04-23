import unittest
import cellyzer.core as core
import cellyzer.io as io
import datetime


class TestCellDataSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # before all the tests
        cls.callDataSet = core.CallDataSet()
        call_file_path = "../../demo/demo_datasets/test_data/calls.csv"
        cls.callDataSet = io.read_call(call_file_path)

        cell_file_path = "../../demo/demo_datasets/test_data/antennas.csv"
        cls.cellDataSet = io.read_cell(cell_file_path, call_dataset_obj=cls.callDataSet)

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
    def test_get_cell_records(self):
        self.assertEqual(len(self.cellDataSet.get_cell_records()), 27)
        self.assertEqual(self.cellDataSet.get_cell_records(1).get_cell_id(), '1')
        self.assertEqual(self.cellDataSet.get_cell_records("1").get_cell_id(), '1')
        self.assertEqual(self.cellDataSet.get_cell_records(1.1), None)

        with self.assertRaises(TypeError):
            self.cellDataSet.get_cell_records([])
            self.cellDataSet.get_cell_records({})

    def test_get_location(self):
        self.assertEqual(self.cellDataSet.get_location(1), (42.366944, -71.083611))
        self.assertEqual(self.cellDataSet.get_location('1'), (42.366944, -71.083611))
        self.assertEqual(self.cellDataSet.get_location('1.1'), None)

        with self.assertRaises(TypeError):
            self.cellDataSet.get_location([])
            self.cellDataSet.get_location({})
            self.cellDataSet.get_location(None)

    def test_get_population(self):
        all_cell_population = [
            {'cell_id': '1', 'latitude': '42.366944', 'longitude': '-71.083611', 'population_around_cell': 1},
            {'cell_id': '2', 'latitude': '42.386722', 'longitude': '-71.138778', 'population_around_cell': 2},
            {'cell_id': '3', 'latitude': '42.3604', 'longitude': '-71.087374', 'population_around_cell': 0},
            {'cell_id': '4', 'latitude': '42.353917', 'longitude': '-71.105', 'population_around_cell': 0},
            {'cell_id': '5', 'latitude': '42.36', 'longitude': '-71.12', 'population_around_cell': 0},
            {'cell_id': '6', 'latitude': '42.375', 'longitude': '-71.1', 'population_around_cell': 0},
            {'cell_id': '7', 'latitude': '42.345', 'longitude': '-71.09', 'population_around_cell': 0},
            {'cell_id': '8', 'latitude': '42.39', 'longitude': '-71.105', 'population_around_cell': 0},
            {'cell_id': '9', 'latitude': '42.38', 'longitude': '-71.09', 'population_around_cell': 0},
            {'cell_id': '10', 'latitude': '42.304917', 'longitude': '-71.147374', 'population_around_cell': 2},
            {'cell_id': '11', 'latitude': '42.373917', 'longitude': '-70.067374', 'population_around_cell': 0},
            {'cell_id': '12', 'latitude': '42.313917', 'longitude': '-71.037374', 'population_around_cell': 0},
            {'cell_id': '13', 'latitude': '42.40944', 'longitude': '-71.1', 'population_around_cell': 0},
            {'cell_id': '14', 'latitude': '42.41', 'longitude': '-71.073', 'population_around_cell': 0},
            {'cell_id': '15', 'latitude': '42.44', 'longitude': '-71.15', 'population_around_cell': 0},
            {'cell_id': '16', 'latitude': '42.48', 'longitude': '-71.23', 'population_around_cell': 0},
            {'cell_id': '17', 'latitude': '42.35', 'longitude': '-71.05', 'population_around_cell': 0},
            {'cell_id': '18', 'latitude': '42.33', 'longitude': '-71.11', 'population_around_cell': 0},
            {'cell_id': '19', 'latitude': '42.36', 'longitude': '-71.25', 'population_around_cell': 0},
            {'cell_id': '20', 'latitude': '42.413', 'longitude': '-71.143', 'population_around_cell': 0},
            {'cell_id': '21', 'latitude': '42.373917', 'longitude': '-71.215', 'population_around_cell': 0},
            {'cell_id': '22', 'latitude': '43.37', 'longitude': '-71.085', 'population_around_cell': 0},
            {'cell_id': '23', 'latitude': '43.39', 'longitude': '-71.11', 'population_around_cell': 0},
            {'cell_id': '24', 'latitude': '42.29', 'longitude': '-71.13', 'population_around_cell': 0},
            {'cell_id': '25', 'latitude': '42.31', 'longitude': '-71.16', 'population_around_cell': 0},
            {'cell_id': '26', 'latitude': '42.313', 'longitude': '-71.135', 'population_around_cell': 0},
            {'cell_id': '27', 'latitude': '42.297', 'longitude': '-71.155', 'population_around_cell': 0}]
        self.assertEqual(self.cellDataSet.get_population(), all_cell_population)

        self.assertEqual(self.cellDataSet.get_population("1"),
                         {'cell_id': '1', 'latitude': '42.366944', 'longitude': '-71.083611',
                          'population_around_cell': 1})
        self.assertEqual(self.cellDataSet.get_population("1.1"), None)
        with self.assertRaises(TypeError):
            self.cellDataSet.get_population([])
            self.cellDataSet.get_population({})

    def test_get_unique_users_around_cell(self):
        test = self.callDataSet.get_records()
        result = ['8d27cf2694', '329233d117', 'bac412f897', '3e97992791', '7331c02864']
        self.assertEqual(self.cellDataSet.get_unique_users_around_cell(test), result)

    def test_check_user_location_matches_cell(self):
        self.assertEqual(self.cellDataSet.check_user_location_matches_cell('3e97992791', 10), True)
        self.assertEqual(self.cellDataSet.check_user_location_matches_cell('3e97992791', 2), False)
        self.assertEqual(self.cellDataSet.check_user_location_matches_cell('3e97992791', 2.2), False)
        self.assertEqual(self.cellDataSet.check_user_location_matches_cell('123', 10), False)

        with self.assertRaises(TypeError):
            self.cellDataSet.check_user_location_matches_cell([], [])
            self.cellDataSet.check_user_location_matches_cell(None, 2)
            self.cellDataSet.check_user_location_matches_cell(2, None)
            self.cellDataSet.check_user_location_matches_cell({}, 2)
            self.cellDataSet.check_user_location_matches_cell(None, [])

    def test_get_trip_details(self):
        result = [{'timestamp': datetime.datetime(2010, 9, 9, 18, 16, 47), 'duration': '0', 'cell_id': '1',
                   'location': (42.366944, -71.083611)},
                  {'timestamp': datetime.datetime(2010, 9, 9, 18, 37, 5), 'duration': '0', 'cell_id': '2',
                   'location': (42.386722, -71.138778)},
                  {'timestamp': datetime.datetime(2010, 9, 9, 19, 3, 5), 'duration': '0', 'cell_id': '2',
                   'location': (42.386722, -71.138778)},
                  {'timestamp': datetime.datetime(2010, 9, 9, 20, 2, 16), 'duration': '0', 'cell_id': '2',
                   'location': (42.386722, -71.138778)},
                  {'timestamp': datetime.datetime(2010, 9, 9, 20, 57, 51), 'duration': '0', 'cell_id': '3',
                   'location': (42.3604, -71.087374)},
                  {'timestamp': datetime.datetime(2010, 9, 9, 22, 7, 39), 'duration': '0', 'cell_id': '3',
                   'location': (42.3604, -71.087374)},
                  {'timestamp': datetime.datetime(2010, 9, 9, 22, 8, 8), 'duration': '0', 'cell_id': '3',
                   'location': (42.3604, -71.087374)},
                  {'timestamp': datetime.datetime(2010, 9, 9, 22, 12, 1), 'duration': '215', 'cell_id': '2',
                   'location': (42.386722, -71.138778)},
                  {'timestamp': datetime.datetime(2010, 9, 9, 22, 38, 9), 'duration': '41', 'cell_id': '2',
                   'location': (42.386722, -71.138778)},
                  {'timestamp': datetime.datetime(2010, 9, 9, 23, 2, 56), 'duration': '0', 'cell_id': '2',
                   'location': (42.386722, -71.138778)},
                  {'timestamp': datetime.datetime(2010, 9, 9, 23, 18, 13), 'duration': '0', 'cell_id': '2',
                   'location': (42.386722, -71.138778)},
                  {'timestamp': datetime.datetime(2010, 9, 9, 23, 21, 5), 'duration': '0', 'cell_id': '2',
                   'location': (42.386722, -71.138778)},
                  {'timestamp': datetime.datetime(2010, 9, 9, 23, 28, 24), 'duration': '4', 'cell_id': '2',
                   'location': (42.386722, -71.138778)},
                  {'timestamp': datetime.datetime(2010, 9, 10, 6, 1, 27), 'duration': '52', 'cell_id': '1',
                   'location': (42.366944, -71.083611)},
                  {'timestamp': datetime.datetime(2010, 9, 10, 6, 4, 43), 'duration': '0', 'cell_id': '2',
                   'location': (42.386722, -71.138778)},
                  {'timestamp': datetime.datetime(2010, 9, 10, 7, 45, 52), 'duration': '39', 'cell_id': '4',
                   'location': (42.353917, -71.105)},
                  {'timestamp': datetime.datetime(2010, 9, 10, 7, 53, 9), 'duration': '0', 'cell_id': '2',
                   'location': (42.386722, -71.138778)},
                  {'timestamp': datetime.datetime(2010, 9, 10, 7, 54, 2), 'duration': '0', 'cell_id': '1',
                   'location': (42.366944, -71.083611)},
                  {'timestamp': datetime.datetime(2010, 9, 10, 11, 15, 49), 'duration': '0', 'cell_id': '10',
                   'location': (42.304917, -71.147374)},
                  {'timestamp': datetime.datetime(2010, 9, 10, 19, 35, 57), 'duration': '0', 'cell_id': '1',
                   'location': (42.366944, -71.083611)}]

        self.assertEqual(self.cellDataSet.get_trip_details("7331c02864"), result)

        with self.assertRaises(TypeError):
            self.cellDataSet.get_trip_details("7331c02864", console_print='str')
            self.cellDataSet.get_trip_details("7331c02864", tabulate='str')
            self.cellDataSet.get_trip_details("7331c02864", console_print='str', tabulate='str')
            self.cellDataSet.get_trip_details(12.3)
            self.cellDataSet.get_trip_details([])
            self.cellDataSet.get_trip_details({})


if __name__ == '__main__':
    unittest.main()
