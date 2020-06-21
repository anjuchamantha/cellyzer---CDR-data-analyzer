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

        # cls.call_csv_test_obj = io.read_call(cls.call_csv_test_path)

    def test_to_json(self):
        with self.assertRaises(TypeError):
            io.to_json("obj", "calls")
            io.to_json(None, "calls")
            io.to_json(io.read_call(self.call_csv_test_path), 123)
            io.to_json(io.read_call(self.call_csv_test_path), None)

    def test_to_csv(self):
        with self.assertRaises(TypeError):
            io.to_csv("obj", "calls")
            io.to_csv(None, "calls")
            io.to_csv(io.read_call(self.call_csv_test_path), 123)
            io.to_csv(io.read_call(self.call_csv_test_path), None)

    def test_read_csv(self):
        with self.assertRaises(TypeError):
            io.read_csv(123)
            io.read_csv(None)

    def test_read_call(self):
        with self.assertRaises(TypeError):
            io.read_call(file_path=123)
            io.read_call(None)
            io.read_call(self.call_csv_test_path, file_type=123)
            io.read_call(self.call_csv_test_path, file_type=None)
            io.read_call(self.call_csv_test_path, hash=123)
            io.read_call(self.call_csv_test_path, hash=None)
            io.read_call(self.call_csv_test_path, splitted_line={})

    def test_read_msg(self):
        with self.assertRaises(TypeError):
            io.read_msg(file_path=123)
            io.read_msg(None)
            io.read_msg(self.msg_csv_test_path, file_type=123)
            io.read_msg(self.msg_csv_test_path, file_type=None)
            io.read_msg(self.msg_csv_test_path, hash=123)
            io.read_msg(self.msg_csv_test_path, hash=None)
            io.read_msg(self.msg_csv_test_path, splitted_line={})

    def test_read_cell(self):
        with self.assertRaises(TypeError):
            io.read_cell(file_path=123)
            io.read_cell(None)
            io.read_cell(self.cell_csv_test_path, call_csv_path=123)
            io.read_cell(self.cell_csv_test_path, call_dataset_obj=io.read_msg(self.msg_csv_test_path))
            io.read_cell(self.cell_csv_test_path, call_dataset_obj="call_data_object")
            io.read_cell(self.cell_csv_test_path, file_type=123)
            io.read_cell(self.cell_csv_test_path, file_type=None)
            io.read_cell(self.cell_csv_test_path, splitted_line={})

    def test_read_xls(self):
        with self.assertRaises(TypeError):
            io.read_xls(filepath=123)
            io.read_xls(filepath=None)
            io.read_xls(filepath=self.call_xlsx_path, call_data_set="data obj")
            io.read_xls(filepath=self.call_xlsx_path, hash="True")
            io.read_xls(filepath=self.call_xlsx_path, hash=None)

    def test_read_json(self):
        with self.assertRaises(TypeError):
            io.read_json(filepath=123)
            io.read_json(filepath=None)
            io.read_json(filepath=self.call_json_path, hash=None)
            io.read_json(filepath=self.call_json_path, hash="True")
            io.read_json(filepath=self.call_json_path, hash=123)

    def test_hash_number(self):
        with self.assertRaises(TypeError):
            io.hash_number(123)
            io.hash_number(None)
            io.hash_number([])

    def test_create_call_obj(self):
        with self.assertRaises(TypeError):
            io.create_call_obj(calls=None, fieldnames=[], hash=True)
            io.create_call_obj(calls={}, fieldnames=[], hash=True)
            io.create_call_obj(calls=[], fieldnames={}, hash=True)
            io.create_call_obj(calls=[], fieldnames=None, hash=True)
            io.create_call_obj(calls=[], fieldnames=[], hash="True")
            io.create_call_obj(calls=[], fieldnames=[], hash=None)

    def test_create_msg_obj(self):
        with self.assertRaises(TypeError):
            io.create_msg_obj(messages=None, fieldnames=[], hash=True)
            io.create_msg_obj(messages={}, fieldnames=[], hash=True)
            io.create_msg_obj(messages=[], fieldnames={}, hash=True)
            io.create_msg_obj(messages=[], fieldnames=None, hash=True)
            io.create_msg_obj(messages=[], fieldnames=[], hash="True")
            io.create_msg_obj(messages=[], fieldnames=[], hash=None)

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
