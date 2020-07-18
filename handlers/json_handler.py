import json
from handlers.base_handler import BaseHandler
from mutators.bufferoverflow_mutator import BufOverflowMutator
from mutators.formatstring_mutator import FormatStringMutator
from mutators.random_byte_mutator import RandomByteMutator
from mutators.integeroverflow_mutator import IntOverflowMutator


class JsonHandler(BaseHandler):
    '''
    Hander for JSON file/input
    '''
    def __init__(self, data: dict, raw_data: str):
        super().__init__(raw_data)
        self._data_dict = data
        self._mutators = []

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

    # TODO: have mutators as class attributes
    def mutate_elem(self, data):
        for mutator in self.mutators:
            mutator.set_input_str(str(data))  # TODO: NEEDS TO BE FIXED MAYBER?
            for mutated_str in mutator.mutate():
                yield mutated_str
        yield data

    def generate_input(self) -> str:
        """
        Generate mutated strings from the initial input file.
        """
        buf_overflow = BufOverflowMutator()
        fmt_str = FormatStringMutator()
        rand_byte = RandomByteMutator()
        self.mutators = [buf_overflow, fmt_str, rand_byte]
        # Feed my hungry mutators
        for mutator in self.mutators:
            mutator.set_input_str(self.data_raw)
            for mutated_str in mutator.mutate():
                yield mutated_str
        # MUTATE each field
        int_overflow = IntOverflowMutator()
        self.mutators = [buf_overflow, fmt_str, rand_byte, int_overflow]
        # Feed my hungry mutators
        for mutated_data in self.mutate_structure(self._data_dict):
            yield json.dumps(mutated_data, indent=4)
