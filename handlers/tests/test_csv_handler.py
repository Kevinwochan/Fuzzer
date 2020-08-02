import unittest
import tempfile
import csv
import os
from handlers.csv_handler import CsvHandler


class CsvHandlerTests(unittest.TestCase):
    """
    Test CsvHandler methods
    """

    def setUp(self):
        self.tmp_file = tempfile.NamedTemporaryFile(mode="w")
        self.test_data = [
            ["some", "header", "string"],
            ["a", "b", "c"],
            ["some", "other", "column"],
        ]
        self.test_data_raw = "some,header,string\na,b,c\nsome,other,column"
        # Write test data to temp file
        with open(self.tmp_file.name, "w") as tmp_csv:
            csv_writer = csv.writer(tmp_csv)
            csv_writer.writerows(self.test_data)
            # Remove last empty line
            tmp_csv.seek(0, os.SEEK_END)
            tmp_csv.seek(tmp_csv.tell() - 2, os.SEEK_SET)
            tmp_csv.truncate()
            # Seek to start
            tmp_csv.flush()
            tmp_csv.seek(0)

        self.handler = CsvHandler(sample_filename=self.tmp_file.name)

    def tearDown(self):
        self.tmp_file.close()

    def test_parse_to_list(self):
        """
        Test that parse_to_list() should return the correct format
        """

        formatted = self.handler.data_list
        self.assertEqual(formatted, self.test_data)

    def test_parse_to_raw(self):
        """
        Test that parse_to_raw() should return the correct format
        Note that there should not be a final empty line like normal
        csv writer behaviour
        """

        formatted = self.handler.data_raw
        self.assertEqual(formatted, self.test_data_raw)

    def test_format_data_list(self):
        """
        Test that format_data_list() should return the correct original format
        """

        formatted = self.handler.format_data_list(self.test_data)
        self.assertEqual(formatted, self.test_data_raw)
