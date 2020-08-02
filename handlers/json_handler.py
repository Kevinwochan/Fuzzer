"""
For mutating a JSON sample file
"""
import json
from handlers.base_handler import BaseHandler
from mutators.super_mutator import SuperMutator


class JsonHandler(BaseHandler):
    '''
    Hander for JSON file/input
    '''

    def __init__(self, data: dict, raw_data: str):
        super().__init__(raw_data)
        self._data_dict = data
        self._mutators = SuperMutator()


    @property
    def mutators(self):
        return self._mutators

    @mutators.setter
    def mutators(self, mutators: list):
        self._mutators = mutators

    def mutate_structure(self, data):
        if isinstance(data, dict):
            for item in self.mutate_dict(data):
                yield item
        elif isinstance(data, list):
            for item in self.mutate_list(data):
                yield item
        else:
            for item in self.mutate_elem(data):
                yield item

    def mutate_dict(self, data):
        for (k, v) in data.items():
            for item in self.mutate_structure(v):
                data[k] = item
                yield data

    def mutate_list(self, data):
        for i, elem in enumerate(data):
            for item in self.mutate_structure(elem):
                data[i] = item
                yield data

    def mutate_elem(self, data) -> str:
        self.mutators.set_input_str(str(data))
        for mutated_str in self.mutators.mutate():
            yield mutated_str
        yield data

    def generate_input(self) -> str:
        """
        Generate mutated strings from the initial input file.
        """
        # Feed my hungry mutators
        self.mutators.set_input_str(self.data_raw)
        for mutated_str in self.mutators.mutate():
            yield mutated_str

        # MUTATE each field
        for mutated_data in self.mutate_structure(self._data_dict):
            yield json.dumps(mutated_data, indent=4)
