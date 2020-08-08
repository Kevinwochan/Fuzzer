"""
For mutating a XML sample file
"""
import xmltodict
import copy
from pwn import cyclic
from handlers.dict_handler import DictionaryHandler


class XMLHandler(DictionaryHandler):
    """
    Hander for XML file/input
    """

    def __init__(self, data: dict, data_raw: str):
        super().__init__(data, data_raw)

    def mutate_dict(self, data: dict) -> dict:
        """
        Mutates each value in dictionary recursively.
        Mutates each key in dictionary recursively,
        except for '#text' key as it is a xmltodict-specific identifer.
        """
        for (k, v) in data.items():
            # Mutate all values recursively
            for item in self.mutate_structure(v):
                dict_copy = copy.deepcopy(data)
                dict_copy[k] = item
                yield dict_copy
            # Mutate keys
            if k[0] in ["@", "#", "!"] and self.is_valid_dict_key(k):
                token = k[0]
                for item in self.mutate_structure(k[1:]):
                    dict_copy = copy.deepcopy(data)
                    # Replace old key with new key
                    dict_copy[f"{token}{item}"] = v
                    dict_copy.pop(k)
                    yield dict_copy

    def generate_duplicate_key_dict(
        self,
        data: dict,
        n_duplicates: int = 256
    ) -> dict:
        """
        Generates dictionary with duplicated keys.
        Ignore xmltodict-specific keys (i.e. #text).
        """
        dict_copy = copy.deepcopy(data)
        for (k, v) in dict_copy.items():
            if self.is_valid_dict_key(k):
                new_dict = copy.deepcopy(dict_copy)
                for i in range(1, n_duplicates):
                    new_key = f"{k}{str(cyclic(i))}"
                    new_dict[new_key] = dict_copy[k]
                    yield new_dict

    def mutate_elem(self, data: str) -> str:
        """
        Mutates a string value.
        Return value has to be a string (xmltodict-specific)
        """
        self.mutators.set_input_str(str(data))
        for mutated_str in self.mutators.mutate():
            yield str(mutated_str)

    def is_valid_dict_key(self, key: str) -> bool:
        """
        Checks whether a key is a valid modifiable xmltodict key.
        I.e. #text will be ignored
        """
        return key != "#text"

    def format_data_dict(self, data: dict) -> str:
        """
        Function to convert a dictionary to string.
        """
        return xmltodict.unparse(data, full_document=False)
