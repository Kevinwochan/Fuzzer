import copy
import json
from handlers.base_handler import BaseHandler
from mutators.bufferoverflow_mutator import BufOverflowMutator
from mutators.formatstring_mutator import FormatStringMutator
from mutators.random_byte_mutator import RandomByteMutator

class JsonHandler(BaseHandler):
    """
    Hander for JSON file/input
    """
    def __init__(self, sample_filename: str):
        super().__init__(sample_filename)
        self._data_parsed = dict()

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

    def generate_input(self) ->str:
        """
        Gnerate mutated strings
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
            for field in enumerate(self.data_list):
                new_data = copy.deepcopy(self.data_list)
                for mutated_str in mutator.mutate():
                    field = mutated_str
                yield self.format_data_list(new_data)
            # MUTATE MY LOVLIES!    

