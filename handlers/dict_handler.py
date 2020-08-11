import copy
import json
from handlers.base_handler import BaseHandler
from mutators.super_mutator import SuperMutator
from pwn import cyclic


class DictionaryHandler(BaseHandler):
    """
    Hander for dictionary objects
    An example dictionary object:
        obj = {
            "dict": {
                "key1": "value1",
                "key2": "value2"
            },
            "dict_list": {
                "list_key": ["item1", "item2"]
            },
            "dict_dict": {
                "0": {
                    ...
                },
                "1": {
                    ...
                }
            },
            "list": ["some","list","items"],
            "list_dict": [{
                "1": "val1",
                "2": "val2"
            },
            {
                "3": "val3",
                "4": "val4"
            }]
        }
    """
    def __init__(self, data: dict, data_raw: str):
        super().__init__(data_raw)
        self._data_dict = data
        self._mutators = SuperMutator()

    @property
    def mutators(self):
        return self._mutators

    @mutators.setter
    def mutators(self, mutators: list):
        self._mutators = mutators

    def mutate_structure(self, data: any) -> dict:
        """
        Recursively mutate each item in a dictionary.
        If data is a dictionary, mutate keys, values and make
        random duplicated keys.
        If data is a list, mutate all element in the list and
        make random duplicated element.
        Otherwise, mutate data using mutators.
        """
        if isinstance(data, dict):
            dict_copy = copy.deepcopy(data)
            for item in self.mutate_dict(dict_copy):
                yield item
            # Duplicate keys
            for mutated_dict in self.generate_duplicate_key_dict(data):
                yield mutated_dict
        elif isinstance(data, list):
            list_copy = copy.deepcopy(data)
            for item in self.mutate_list(list_copy):
                yield item
            # Duplicate random item
            for mutated_list in self.generate_duplicate_list_items(data):
                yield mutated_list
        else:
            for item in self.mutate_elem(data):
                yield item

    def mutate_dict(self, data: dict) -> dict:
        """
        Mutates each value in dictionary recursively.
        Mutates each key in dictionary recursively.
        """
        for (k, v) in data.items():
            # Mutate all values recursively
            for item in self.mutate_structure(v):
                dict_copy = copy.deepcopy(data)
                dict_copy[k] = item
                yield dict_copy
            # Mutate keys
            for item in self.mutate_structure(k):
                dict_copy = copy.deepcopy(data)
                # Replace old key with new key
                dict_copy[item] = v
                dict_copy.pop(k)
                yield dict_copy

    def mutate_list(self, data: list) -> dict:
        """
        Mutates each item in a list recursively.
        """
        # Mutate each item
        for i, elem in enumerate(data):
            for item in self.mutate_structure(elem):
                list_copy = copy.deepcopy(data)
                list_copy[i] = item
                yield list_copy

    def mutate_elem(self, data: str) -> any:
        """
        Mutates a string value.
        """
        self.mutators.set_input_str(str(data))
        for mutated_str in self.mutators.mutate():
            yield mutated_str

    def generate_duplicate_key_dict(self,
                                    data: dict,
                                    n_duplicates: int = 256) -> dict:
        """
        Generates a dictionary with duplicated keys.
        Default duplications: 256.
        """
        dict_copy = copy.deepcopy(data)
        for (k, v) in dict_copy.items():
            new_dict = copy.deepcopy(dict_copy)
            for i in range(1, n_duplicates):
                new_key = f"{k}{str(cyclic(i))}"
                new_dict[new_key] = dict_copy[k]
                yield new_dict

    def generate_duplicate_list_items(self,
                                      data: list,
                                      n_duplicates: int = 256) -> list:
        """
        Generates a list with duplicated items.
        Default duplications: 256.
        """
        for elem in data:
            list_copy = copy.deepcopy(data)
            elems = [elem] * n_duplicates
            list_copy.append(elems)
            yield list_copy

    def format_data_dict(self, data: dict) -> str:
        """
        Function to convert a dictionary to string.
        Default: json.dumps(data, indent=4).
        """
        return json.dumps(data, indent=4)

    def generate_raw_duplicate(self):
        for i in range(1,9):
            yield self.data_raw * (10**i)

    def generate_input(self) -> str:
        """
        Generate mutated strings from the initial input file.
        """
        # Feed my hungry mutators
        self.mutators.set_input_str(self.data_raw)
        for mutated_str in self.mutators.mutate():
            yield mutated_str

        # Duplicates raw data
        # n_duplicates = 10**7
        # yield self.data_raw * n_duplicates

        # Mutate values
        for mutated_data in self.mutate_structure(self._data_dict):
            yield self.format_data_dict(mutated_data)
