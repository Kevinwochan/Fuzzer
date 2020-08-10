import copy
import json
import sys
import os
import copy

sys.path.append('/home/ubuntu/fuzzer/')

from handlers.base_handler import BaseHandler
from mutators.super_mutator import SuperMutator
from pwn import cyclic


class InfiniteHandler(BaseHandler):
    def __init__(self, data: any, data_raw: str):
        super().__init__(data_raw)
        self._mutators = SuperMutator()
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

    def generate_input(self) -> str:
        """
        Gnerate mutated strings
        """
        field_mutators = [
            SuperMutator(str(field)).mutate() for field in self._fields
        ]
        counter = 10
        while True:
            counter -= 1
            if counter == 0:
                break
            for index, field in enumerate(self._fields):
                mutated_data = next(field_mutators[index], None)
                if mutated_data is None:
                    continue
                copied_data = copy.deepcopy(self._fields)
                copied_data[index] = mutated_data
                yield self.construct(self._structure, copied_data)


if __name__ == '__main__':
    print('=' * 10)
    d = InfiniteHandler([['a'], ['b'], ['c']], 'a\nb\nc')
    d.generate_input()
    print('=' * 10)
    d = InfiniteHandler({'a': 'b', 'c': 'd'}, '{\n"a":"b",\n"c":"d"\n}')
    d.generate_input()
    print('=' * 10)
'''
    Example:
    Input:
    structure = {'hello': 1, 'hey': ['far', 2]}
    mudateted_data = ['hello', 1 ,'AAAAAAA', 'far', 2]
    Output:
    {'hello': 1, 'AAAAAA': ['far', 2]}
    recursive call to decompose complex JSON into a flat list
    Example:
    Input:
    data = {'hello': 1, 'hey': ['far', 2]}
    Output:
    ['hello', 1 ,'hey', 'far', 2]
'''
