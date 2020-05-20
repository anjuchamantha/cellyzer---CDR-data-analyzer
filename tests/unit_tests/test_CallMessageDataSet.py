import unittest
import cellyzer.core as core
import cellyzer.io as io


class TestCallMessageDataSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # before all the tests
        cls.user1 = "3e97992791"
        cls.user2 = "265034e175"
        cls.user3 = '329233d117'

        cls.callDataSet = core.CallDataSet()
        call_file_path = "../../demo/demo_datasets/test_data/calls.csv"
        cls.callDataSet = io.read_call(call_file_path)

        cls.msgDataSet = core.MessageDataSet()
        msg_file_path = "../../demo/demo_datasets/test_data/messages.csv"
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
        self.assertEqual(len(self.callDataSet.get_records()), 49)
        self.assertEqual(len(self.callDataSet.get_records(self.user1)), 13)
        self.assertEqual(len(self.msgDataSet.get_records(123)), 0)
        self.assertEqual(len(self.callDataSet.get_records(self.user1, self.user2)), 4)

        with self.assertRaises(TypeError):
            self.callDataSet.get_records(user1=12.3)
            self.msgDataSet.get_records(user1=[self.user1])
            self.callDataSet.get_records(user2={self.user2})

    def test_get_all_users(self):
        call_users = ['8d27cf2694', '373a4fb419', '329233d117', '6cfc4bd054', 'e98994c239', '0041628436', 'bac412f897',
                      '11fb537495', '322692e582', 'c21b973441', '3e97992791', '64e7321526', '2bc2488066', '2f78602598',
                      '377415d768', '265034e175', '5973bd0224', '7331c02864', 'f23eb82163', '2914c2d+31', 'e967db9452',
                      'ca69f5a563', '380c65b156', '0c47c9c382', '1ed77db846']

        self.assertEqual(self.callDataSet.get_all_users(), call_users)

        msg_users = ['8d27cf2694', '78c4ca6671', '329233d117', '0041628436', 'bac412f897', '322692e582', 'e1ba3ba266',
                     'ae578bf678', '30b785e895']
        self.assertEqual(self.msgDataSet.get_all_users(), msg_users)

    def test_get_connected_users(self):
        user1_connections_calls = ['64e7321526', '2bc2488066', '2f78602598', '377415d768', '265034e175', '5973bd0224']
        self.assertEqual(self.callDataSet.get_connected_users(self.user1), user1_connections_calls)
        user3_connections_msgs = ['0041628436', 'bac412f897']
        self.assertEqual(self.msgDataSet.get_connected_users(self.user3), user3_connections_msgs)

        with self.assertRaises(TypeError):
            self.callDataSet.get_connected_users(None)
            self.callDataSet.get_connected_users(12.3)
            self.callDataSet.get_connected_users([self.user1])
            self.callDataSet.get_connected_users({self.user1})

    def test_print_connection_matrix(self):
        pass

    def test_get_connections(self):
        call_connections = [['373a4fb419', '8d27cf2694'], ['329233d117', '6cfc4bd054'], ['e98994c239', '329233d117'],
                            ['329233d117', '0041628436'], ['329233d117', '0041628436'], ['0041628436', '329233d117'],
                            ['329233d117', 'bac412f897'], ['11fb537495', '329233d117'], ['bac412f897', '322692e582'],
                            ['bac412f897', 'c21b973441'], ['bac412f897', '322692e582'], ['bac412f897', '322692e582'],
                            ['bac412f897', '322692e582'], ['bac412f897', 'c21b973441'], ['bac412f897', '322692e582'],
                            ['bac412f897', '329233d117'], ['3e97992791', '64e7321526'], ['3e97992791', '2bc2488066'],
                            ['3e97992791', '2bc2488066'], ['3e97992791', '2f78602598'], ['3e97992791', '2f78602598'],
                            ['3e97992791', '377415d768'], ['3e97992791', '265034e175'], ['3e97992791', '265034e175'],
                            ['5973bd0224', '3e97992791'], ['3e97992791', '265034e175'], ['3e97992791', '377415d768'],
                            ['3e97992791', '377415d768'], ['3e97992791', '265034e175'], ['7331c02864', 'f23eb82163'],
                            ['7331c02864', 'f23eb82163'], ['7331c02864', 'f23eb82163'], ['7331c02864', '2914c2d+31'],
                            ['7331c02864', 'f23eb82163'], ['7331c02864', '2914c2d+31'], ['7331c02864', '2914c2d+31'],
                            ['7331c02864', 'f23eb82163'], ['7331c02864', 'e967db9452'], ['7331c02864', 'ca69f5a563'],
                            ['7331c02864', '380c65b156'], ['7331c02864', '322692e582'], ['7331c02864', 'e967db9452'],
                            ['7331c02864', 'e967db9452'], ['7331c02864', 'f23eb82163'], ['7331c02864', 'e967db9452'],
                            ['7331c02864', '0041628436'], ['7331c02864', '0041628436'], ['7331c02864', '0c47c9c382'],
                            ['7331c02864', '1ed77db846']]

        self.assertEqual(self.callDataSet.get_connections(allow_duplicates=True), call_connections)

        msg_connections = [['78c4ca6671', '8d27cf2694'], ['0041628436', '329233d117'], ['329233d117', '0041628436'],
                           ['329233d117', 'bac412f897'], ['bac412f897', '322692e582'], ['322692e582', 'bac412f897'],
                           ['bac412f897', '322692e582'], ['322692e582', 'bac412f897'], ['bac412f897', '322692e582'],
                           ['322692e582', 'bac412f897'], ['bac412f897', '322692e582'], ['322692e582', 'bac412f897'],
                           ['322692e582', 'bac412f897'], ['bac412f897', '322692e582'], ['0041628436', 'bac412f897'],
                           ['bac412f897', '0041628436'], ['0041628436', 'bac412f897'], ['bac412f897', '0041628436'],
                           ['329233d117', 'bac412f897'], ['bac412f897', '322692e582'], ['322692e582', 'bac412f897'],
                           ['bac412f897', '322692e582'], ['322692e582', 'bac412f897'], ['e1ba3ba266', 'bac412f897'],
                           ['ae578bf678', 'bac412f897'], ['30b785e895', 'bac412f897'], ['bac412f897', '30b785e895'],
                           ['30b785e895', 'bac412f897'], ['bac412f897', '322692e582'], ['329233d117', 'bac412f897'],
                           ['bac412f897', '329233d117'], ['322692e582', 'bac412f897'], ['bac412f897', '322692e582'],
                           ['322692e582', 'bac412f897'], ['bac412f897', '322692e582'], ['322692e582', 'bac412f897'],
                           ['bac412f897', '322692e582'], ['322692e582', 'bac412f897'], ['bac412f897', '322692e582'],
                           ['322692e582', 'bac412f897'], ['bac412f897', '322692e582'], ['322692e582', 'bac412f897'],
                           ['bac412f897', '322692e582'], ['322692e582', 'bac412f897'], ['bac412f897', '322692e582'],
                           ['322692e582', 'bac412f897'], ['bac412f897', '322692e582'], ['322692e582', 'bac412f897'],
                           ['bac412f897', '322692e582']]

        self.assertEqual(self.msgDataSet.get_connections(allow_duplicates=True), msg_connections)


if __name__ == '__main__':
    unittest.main()
