import unittest
import cellyzer.core as core
import cellyzer.io as io


class TestMessageDataSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # before all the tests
        cls.user1 = "7681546436"
        cls.user2 = "7641036117"

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

    def test_get_close_contacts(self):
        user1_result = {'7981267897': 4, '7641036117': 2}
        self.assertEqual(self.msgDataSet.get_close_contacts(user=self.user1, top_contact=2), user1_result)
        self.assertEqual(self.msgDataSet.get_close_contacts(user=self.user1, top_contact='2'), user1_result)

        user2_result = {'7981267897': 4, '7681546436': 2}
        self.assertEqual(self.msgDataSet.get_close_contacts(user=self.user2), user2_result)

        with self.assertRaises(TypeError):
            self.msgDataSet.get_close_contacts(12.3)
            self.msgDataSet.get_close_contacts([self.user1])
            self.msgDataSet.get_close_contacts({1})
            self.msgDataSet.get_close_contacts(None, None)
            self.msgDataSet.get_close_contacts(user=self.user1, top_contact=None)
            self.msgDataSet.get_close_contacts(user=self.user1, top_contact=12.3)
            self.msgDataSet.get_close_contacts(user=self.user1, top_contact=[1])
            self.msgDataSet.get_close_contacts(user=self.user1, top_contact={1})


if __name__ == '__main__':
    unittest.main()
