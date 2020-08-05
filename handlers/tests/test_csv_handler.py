import unittest.loader
from handlers.csv_handler import CsvHandler


class CsvHandlerTests(unittest.TestCase):
    """
    Test CsvHandler methods
    """

    def setUp(self):
        self.test_data = [
            ["some", "header", "string"],
            ["a", "b", "c"],
            ["some", "other", "column"],
        ]
        self.test_data_raw = "some,header,string\na,b,c\nsome,other,column"
        self.handler = CsvHandler(
            data_list=self.test_data,
            data_raw=self.test_data_raw
        )

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
