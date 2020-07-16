import copy
import json
from handlers.base_handler import BaseHandler
from mutators.bufferoverflow_mutator import BufOverflowMutator
from mutators.formatstring_mutator import FormatStringMutator
from mutators.random_byte_mutator import RandomByteMutator

# pylint: disable=no-value-for-parameter
class JsonHandler(BaseHandler):
    """
    Hander for JSON file/input
    """
    def __init__(self, sample_filename: str):
        super().__init__(sample_filename)
        self._data_parsed = dict()

    def parse_to_raw(self) -> str:
        return self._data_raw

    def parse_to_list(self) -> list:
        '''
            decomposes JSON into an simple array of data
            parsed_sample = {"0": 1, "2": 3}
            self.sample = {
                "0": 1,
                "2": 3
            }
            self._data = ["0", 1, "2", 3]
        '''
        with open(self.sample_filename, "r") as f:
            sample_input = f.read().replace('\n', '')
            self._data_parsed = json.loads(sample_input)
            data = self.decompose(self._data_parsed)
            return data
        return []

    @classmethod
    def decompose(self, data) -> list:
        '''
            recursive call to decompose complex JSON into a flat list
            Example:
            Input:
            data = {'hello': 1, 'hey': ['far', 2]}

            Output:
            ['hello', 1 ,'hey', 'far', 2]
        '''
        if isinstance(data, list): 
            accumulator = []
            for item in data:
                accumulator += self.decompose(item)
            return accumulator
        elif isinstance(data, dict): 
            accumulator = []
            for key, val in data.items():
                accumulator.append(key)
                accumulator += self.decompose(val)
            return accumulator
        elif isinstance(data, (str, int, float, bool)):
            return [data]

        raise TypeError('JSON data type not recognised')

    @classmethod
    def construct(self, structure, mutated_data):
        '''
            Example:
            Input:
            structure = {'hello': 1, 'hey': ['far', 2]}
            mudateted_data = ['hello', 1 ,'AAAAAAA', 'far', 2]

            Output:
            {'hello': 1, 'AAAAAA': ['far', 2]}
        '''
        if isinstance(structure, list): 
            return [self.construct(item, mutated_data) for item in structure]
        elif isinstance(structure, dict): 
            accumulator = dict()
            for key, val in structure.items():
                key = mutated_data.pop(0)
                val = self.construct(val, mutated_data)
                accumulator[key] = val
            return accumulator
        elif isinstance(structure, (str, int, float, bool)):
            return mutated_data.pop(0)
        raise TypeError('JSON data type not recognised')

    def format_data_list(self, data: list) -> str:
        """
        Given a list of data types, return a complete json string
        the json will have the same format as the sample input
        """
        mutated_input = self.construct(self._data_parsed, data)
        return json.dumps(mutated_input)

    def do_the_thing(self, parent, item, mutators):
        '''
        iterates through to child elements of a tree
        permutes all possible mutation on each child
        '''
        if isinstance(parent, dict):
            (key, value) = item
            # recursive cases
            if isinstance(value, list):
                value = self.traverse_list(item)
            elif isinstance(value, dict):
                value = self.traverse_dict(item)
            else:
                for mutator in mutators:
                    mutator.set_input_str(value)
                    save = parent[key]
                    for mutated_str in mutator.mutate():
                        parent[key] = mutated_str
                        yield parent
                    parent[key] = save

        # item can't break down further in list
        elif isinstance(parent, list):
            (index, value) = item
            if isinstance(item, list):
                item = self.traverse_list(item)
            elif isinstance(item, dict):
                item = self.traverse_dict(item)
            else: # int, string, etc
                for mutator in mutators:
                    mutator.set_input_str(item)
                    for mutated_str in mutator.mutate():
                        parent[index] = mutated_str
                        yield parent
                parent[index] = item

    def traverse_dict(self, data: dict, mutators) -> dict:
        for key, value in enumerate(data.items()):
            data[key] = self.do_the_thing((key, value), mutators)
            yield data
    
    def traverse_list(self, data: list, mutators) -> list:
        for (index, value) in enumerate(data):
            data[index] = self.do_the_thing((index, value), mutators)
            yield data

    def generate_input(self) -> str:
        """
        Generate mutated strings from the initial input file.
        """
        buf_overflow = BufOverflowMutator()
        fmt_str = FormatStringMutator()
        rand_byte = RandomByteMutator()
        mutators = [buf_overflow, fmt_str, rand_byte]
        # Feed my hungry mutators
        for mutator in mutators:
            # mutate using raw string
            mutator.set_input_str(self.data_raw)
            for mutated_str in mutator.mutate():
                yield mutated_str

        # MUTATE each field
        yield self.traverse_dict(self.data_dict, mutators)
        # MUTATE MY LOVLIES!    
