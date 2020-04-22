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
        self.assertEqual(len(self.callDataSet.get_records()), 46)
        self.assertEqual(len(self.callDataSet.get_records(self.user1)), 13)
        self.assertEqual(len(self.msgDataSet.get_records(123)), 0)
        self.assertEqual(len(self.callDataSet.get_records(self.user1, self.user2)), 4)

        with self.assertRaises(TypeError):
            self.callDataSet.get_records(user1=12.3)
            self.msgDataSet.get_records(user1=[self.user1])
            self.callDataSet.get_records(user2={self.user2})

    def test_get_all_users(self):
        call_users = ['7610039694', '7434677419', '7641036117', '1666472054', '7371326239', '7681546436', '7981267897',
                      '7588304495', '7784425582', '7743039441', '7163185791', '1850897526', '7066875066', '7691640598',
                      '8704500768', '7187432175', '7230262224', '7110730864', '7209670163', '452', '563', '7501874156',
                      '7914559382', '1258345846']
        self.assertEqual(self.callDataSet.get_all_users(), call_users)

        msg_users = ['7610039694', '7684763671', '7641036117', '7681546436', '7981267897', '7784425582', '7033434266',
                     '7817341678', '7541477895']
        self.assertEqual(self.msgDataSet.get_all_users(), msg_users)

    def test_get_connected_users(self):
        user1_connections_calls = ['1850897526', '7066875066', '7691640598', '8704500768', '7187432175', '7230262224']
        self.assertEqual(self.callDataSet.get_connected_users(self.user1), user1_connections_calls)
        user3_connections_msgs = ['7681546436', '7981267897']
        self.assertEqual(self.msgDataSet.get_connected_users(self.user3), user3_connections_msgs)

        with self.assertRaises(TypeError):
            self.callDataSet.get_connected_users(None)
            self.callDataSet.get_connected_users(12.3)
            self.callDataSet.get_connected_users([self.user1])
            self.callDataSet.get_connected_users({self.user1})

    def test_print_connection_matrix(self):
        pass

    def test_get_connections(self):
        call_connections = [['7434677419', '7610039694'], ['7641036117', '1666472054'], ['7371326239', '7641036117'],
                            ['7641036117', '7681546436'], ['7641036117', '7681546436'], ['7681546436', '7641036117'],
                            ['7641036117', '7981267897'], ['7588304495', '7641036117'], ['7981267897', '7784425582'],
                            ['7981267897', '7743039441'], ['7981267897', '7784425582'], ['7981267897', '7784425582'],
                            ['7981267897', '7784425582'], ['7981267897', '7743039441'], ['7981267897', '7784425582'],
                            ['7981267897', '7641036117'], ['7163185791', '1850897526'], ['7163185791', '7066875066'],
                            ['7163185791', '7066875066'], ['7163185791', '7691640598'], ['7163185791', '7691640598'],
                            ['7163185791', '8704500768'], ['7163185791', '7187432175'], ['7163185791', '7187432175'],
                            ['7230262224', '7163185791'], ['7163185791', '7187432175'], ['7163185791', '8704500768'],
                            ['7163185791', '8704500768'], ['7163185791', '7187432175'], ['7110730864', '7209670163'],
                            ['7110730864', '7209670163'], ['7110730864', '7209670163'], ['7110730864', '7209670163'],
                            ['7110730864', '7209670163'], ['7110730864', '452'], ['7110730864', '563'],
                            ['7110730864', '7501874156'], ['7110730864', '7784425582'], ['7110730864', '452'],
                            ['7110730864', '452'], ['7110730864', '7209670163'], ['7110730864', '452'],
                            ['7110730864', '7681546436'], ['7110730864', '7681546436'], ['7110730864', '7914559382'],
                            ['7110730864', '1258345846']]
        self.assertEqual(self.callDataSet.get_connections(), call_connections)

        msg_connections = [['7684763671', '7610039694'], ['7681546436', '7641036117'], ['7641036117', '7681546436'],
                           ['7641036117', '7981267897'], ['7981267897', '7784425582'], ['7784425582', '7981267897'],
                           ['7981267897', '7784425582'], ['7784425582', '7981267897'], ['7981267897', '7784425582'],
                           ['7784425582', '7981267897'], ['7981267897', '7784425582'], ['7784425582', '7981267897'],
                           ['7784425582', '7981267897'], ['7981267897', '7784425582'], ['7681546436', '7981267897'],
                           ['7981267897', '7681546436'], ['7681546436', '7981267897'], ['7981267897', '7681546436'],
                           ['7641036117', '7981267897'], ['7981267897', '7784425582'], ['7784425582', '7981267897'],
                           ['7981267897', '7784425582'], ['7784425582', '7981267897'], ['7033434266', '7981267897'],
                           ['7817341678', '7981267897'], ['7541477895', '7981267897'], ['7981267897', '7541477895'],
                           ['7541477895', '7981267897'], ['7981267897', '7784425582'], ['7641036117', '7981267897'],
                           ['7981267897', '7641036117'], ['7784425582', '7981267897'], ['7981267897', '7784425582'],
                           ['7784425582', '7981267897'], ['7981267897', '7784425582'], ['7784425582', '7981267897'],
                           ['7981267897', '7784425582'], ['7784425582', '7981267897'], ['7981267897', '7784425582'],
                           ['7784425582', '7981267897'], ['7981267897', '7784425582'], ['7784425582', '7981267897'],
                           ['7981267897', '7784425582'], ['7784425582', '7981267897'], ['7981267897', '7784425582'],
                           ['7784425582', '7981267897'], ['7981267897', '7784425582'], ['7784425582', '7981267897'],
                           ['7981267897', '7784425582']]
        self.assertEqual(self.msgDataSet.get_connections(), msg_connections)


if __name__ == '__main__':
    unittest.main()
