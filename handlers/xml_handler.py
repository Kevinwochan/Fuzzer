import xmltodict
import copy
from typing import List
from handlers.base_handler import BaseHandler
from mutators.base_mutator import BaseMutator
from mutators.bufferoverflow_mutator import BufOverflowMutator
from mutators.formatstring_mutator import FormatStringMutator
from mutators.random_byte_mutator import RandomByteMutator
from mutators.integeroverflow_mutator import IntOverflowMutator


class XMLHandler(BaseHandler):
    '''
    Hander for JSON file/input
    '''
    def __init__(self, data: dict, raw_data: str):
        super().__init__(raw_data)
        self._data_dict = data
        buf_overflow = BufOverflowMutator()
        fmt_str = FormatStringMutator()
        rand_byte = RandomByteMutator()
        self.mutators = [buf_overflow, fmt_str, rand_byte]

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
        new_data = copy.deepcopy(data)
        for (k, v) in data.items():
            for item in self.mutate_structure(v):
                data[k] = item
                yield data
        for (k, v) in new_data.items():
            if (k[0] == '@'):
                for item in self.mutate_structure(k[1:]):
                    new_data_2 = copy.deepcopy(new_data)
                    new_data_2[f"{k[0]}{item}"] = new_data[k]
                    new_data_2.pop(k)
                    yield new_data_2

    def mutate_list(self, data):
        for i, elem in enumerate(data):
            for item in self.mutate_structure(elem):
                data[i] = item
                yield data

    """
    <asdadasdasdasd ajsdhfajklsdfhasdfkja="https://">link</asdadasdasdasd>


    "head": {
    "@ajsdhfajklsdfhasdfkja": "https://",
    "#text": "link" 
    }
    """
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
        for mutator in self.mutators:
            mutator.set_input_str(self.data_raw)
            for mutated_str in mutator.mutate():
                yield mutated_str
        for mutated_data in self.mutate_structure(self._data_dict):
            yield xmltodict.unparse(mutated_data,full_document=False)