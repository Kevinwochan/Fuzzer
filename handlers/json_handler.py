import json
from typing import List
from handlers.base_handler import BaseHandler
from mutators.base_mutator import BaseMutator
from mutators.bufferoverflow_mutator import BufOverflowMutator
from mutators.formatstring_mutator import FormatStringMutator
from mutators.random_byte_mutator import RandomByteMutator
from mutators.integeroverflow_mutator import IntOverflowMutator


class JsonHandler(BaseHandler):
    '''
    Hander for JSON file/input
    '''
    def __init__(self, sample_filename: str):
        super().__init__(sample_filename)
        self._data_dict = self.parse_to_dict()
        buf_overflow = BufOverflowMutator()
        fmt_str = FormatStringMutator()
        rand_byte = RandomByteMutator()
        self.mutators = [buf_overflow, fmt_str, rand_byte]

    @property
    def mutators(self) -> List[BaseMutator]:
        return self._mutators

    @mutators.setter
    def mutators(self, mutators: list):
        self._mutators = mutators

    def parse_to_raw(self) -> str:
        with open(self.sample_filename, "r") as txt_file:
            raw_data = txt_file.read()
            # Remove last blank line if exists
            raw_data = raw_data.rstrip()
            return raw_data
        return ""

    def parse_to_dict(self) -> dict:
        with open(self.sample_filename, "r") as f:
            return json.load(f)
        return dict()

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
        for mutator in self.mutators:
            mutator.set_input_str(str(data))
            for mutated_str in mutator.mutate():
                yield mutated_str
        yield data

    def generate_input(self) -> str:
        """
        Generate mutated strings from the initial input file.
        """
        # Feed my hungry mutators
        for mutator in self.mutators:
            mutator.set_input_str(self.data_raw)
            for mutated_str in mutator.mutate():
                yield mutated_str
        # MUTATE each field
        for mutated_data in self.mutate_structure(self._data_dict):
            yield json.dumps(mutated_data, indent=4)
