import unittest
import cellyzer.io as io


class TestIO(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # before all the tests
        cls.call_csv_test_path = "../../demo/demo_datasets/test_data/calls.csv"
        cls.msg_csv_test_path = "../../demo/demo_datasets/test_data/messages.csv"
        cls.cell_csv_test_path = "../../demo/demo_datasets/test_data/antennas.csv"

        cls.call_csv_long_path = "../../demo/demo_datasets/long_data/calls_.csv"
        cls.msg_csv_long_path = "../../demo/demo_datasets/long_data/messages_.csv"
        cls.cell_csv_long_path = "../../demo/demo_datasets/long_data/antennas.csv"

        cls.call_xlsx_path = "../../demo/demo_datasets/test_data/excel data/calls.xlsx"
        cls.msg_xlsx_path = "../../demo/demo_datasets/test_data/excel data/messages.xlsx"
        cls.cell_xlsx_path = "../../demo/demo_datasets/test_data/excel data/cell.xlsx"

        cls.call_json_path = "../../demo/demo_datasets/test_data/json data/call.json"
        cls.msg_json_path = "../../demo/demo_datasets/test_data/json data/message.json"
        cls.cell_json_path = "../../demo/demo_datasets/test_data/json data/cell.json"

    def test_to_json(self):
        pass

    def test_to_csv(self):
        pass

    def test_read_csv(self):
        pass

    def test_read_call(self):
        pass

    def test_read_msg(self):
        pass

    def test_read_cell(self):
        pass

    def test_reas_xls(self):
        pass

    def test_read_json(self):
        pass

    def test_hash_number(self):
        pass

    def test_create_call_obj(self):
        pass

    def test_create_msg_obj(self):
        pass

    def test_create_cell_obj(self):
        pass

    def test_filter_calls(self):
        pass

    def test_filter_messages(self):
        pass

    def test_filter_cells(self):
        pass

    def test_parse_records(self):
        pass

    def test_make_json_from_data(self):
        pass

    def test_xls_to_dict(self):
        pass

    def test_float_to_int(self):
        pass


if __name__ == '__main__':
    unittest.main()
