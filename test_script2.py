import unittest
import os
import yaml
from script2 import bin_to_str, interpret

class TestScript2(unittest.TestCase):
    def setUp(self):
        self.test_bin_file = "test.bin"
        self.test_out_file = "test_output.yaml"
        self.test_memory_range = (0, 10)

    def tearDown(self):
        if os.path.exists(self.test_bin_file):
            os.remove(self.test_bin_file)
        if os.path.exists(self.test_out_file):
            os.remove(self.test_out_file)

    def write_test_data(self, data):
        with open(self.test_bin_file, "wb") as f:
            f.write(bytes(data))

    def test_bin_to_str(self):
        self.write_test_data([97, 10, 101])
        result = bin_to_str(self.test_bin_file)
        expected = ["01100001", "00001010", "01100101"]
        self.assertEqual(result, expected)



    def test_interpret_empty_file(self):
        # Проверка на пустой файл
        self.write_test_data([])
        with self.assertRaises(ValueError):
            interpret(self.test_bin_file, self.test_out_file, self.test_memory_range)

    def test_interpret_incomplete_instruction(self):
        # Неполная инструкция LOAD
        self.write_test_data([97, 0])
        with self.assertRaises(IndexError):
            interpret(self.test_bin_file, self.test_out_file, self.test_memory_range)

if __name__ == "__main__":
    unittest.main()
