"""
For mutating a JSON sample file
"""
import json
from handlers.dict_handler import DictionaryHandler


class JsonHandler(DictionaryHandler):
    """
    Hander for JSON file/input
    """

    def __init__(self, data_dict: dict, data_raw: str):
        super().__init__(data_dict, data_raw)

    def format_data_dict(self, data: dict) -> str:
        """
        Function to convert a dictionary to string.
        """
        return json.dumps(data, indent=4)
