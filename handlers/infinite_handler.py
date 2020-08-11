import sys
sys.path.append('/home/ubuntu/fuzzer/')  # TODO: remove

import copy
from handlers.base_handler import BaseHandler
from mutators.infinite_mutator import InfiniteMutator
from pwn import cyclic


class InfiniteHandler(BaseHandler):
    def __init__(self, data: any, data_raw: str):
        super().__init__(data_raw)
        self._fields = self.decompose(data)
        self._structure = data

    def decompose(self, data) -> list:
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
        else:
            return [data]

    def construct(self, structure, mutated_data):
        if isinstance(structure, list):
            return [self.construct(item, mutated_data) for item in structure]
        elif isinstance(structure, dict):
            accumulator = dict()
            for key, val in structure.items():
                key = mutated_data.pop(0)
                val = self.construct(val, mutated_data)
                accumulator[key] = val
            return accumulator
        else:
            return mutated_data.pop(0)

    def generate_input(self, stop=-1) -> str:
        """
        Gnerate mutated strings
        """
        field_mutators = [
            InfiniteMutator(str(field)).mutate() for field in self._fields
        ]
        counter = 0
        while counter < stop or stop == -1:
            for index, field in enumerate(self._fields):
                mutated_data = next(field_mutators[index], None)
                if mutated_data is None:
                    continue
                copied_data = copy.deepcopy(self._fields)
                copied_data[index] = mutated_data
                yield self.construct(self._structure, copied_data)


'''
if __name__ == '__main__':  # TODO: remove
    print('=' * 10)
    d = InfiniteHandler([['a'], ['b'], ['c']], 'a\nb\nc')
    print(list(d.generate_input(stop=10)))
    print('=' * 10)
    d = InfiniteHandler({'a': 'b', 'c': 'd'}, '{\n"a":"b",\n"c":"d"\n}')
    print(list(d.generate_input(stop=10)))
    print('=' * 10)
'''
