import unittest
import tempfile
import json
import os
from handlers.json_handler import JsonHandler

class JsonHandlerTests(unittest.TestCase):
    """
    Test JsonHandler methods
    """

    def setUp(self):
        self.tmp_file = tempfile.NamedTemporaryFile(mode="w")
        self.test_data = {"len":12, "input":"AAAABBBBCCCC", "more_data":["a","bb"]}
        self.test_data_list = ["len",12, "input","AAAABBBBCCCC", "more_data", "a","bb"]
        self.test_data_raw = '{\n"len": 12,\n"input": "AAAABBBBCCCC",\n"more_data": ["a", "bb"]\n}'
        # Write test data to temp file
        with open(self.tmp_file.name, "w") as tmp_json:
            json.dump(self.test_data, tmp_json, indent=4) # indenting matches samples
        self.handler = JsonHandler(sample_filename=self.tmp_file.name)

    def tearDown(self):
        self.tmp_file.close()

    def test_parse_to_raw(self):
        """
        Test that parse_to_raw() should return the correct format
        """

        formatted = self.handler.data_raw
        self.assertEqual(formatted, self.test_data_raw)
