import unittest
import yaml
from script import assemble
import os


class TestAssembler(unittest.TestCase):
    def setUp(self):
        self.input_file = "test_input.txt"
        self.output_file = "test_output.bin"
        self.log_file = "test_log.yaml"
        with open(self.input_file, 'w') as f:
            f.write("LOAD 1 20\nREAD 2 15\nWRITE 3 2 10\nSUB 1 2 3 4\n")

    def tearDown(self):
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_assemble_creates_binary_and_log(self):
        assemble(self.input_file, self.output_file, self.log_file)

        self.assertTrue(os.path.exists(self.output_file), "Output binary file was not created.")
        self.assertTrue(os.path.exists(self.log_file), "Log file was not created.")

        with open(self.log_file, 'r') as f:
            log_data = yaml.safe_load(f)
            self.assertEqual(len(log_data), 4, "Log file does not have all instructions logged.")

    def test_unknown_command(self):
        with open(self.input_file, 'w') as f:
            f.write("UNKNOWN 1 2 3\n")
        with self.assertRaises(ValueError):
            assemble(self.input_file, self.output_file, self.log_file)


if __name__ == '__main__':
    unittest.main()
