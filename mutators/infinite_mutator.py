"""
A mutator that will provide an infinite amount of mutations for a given string
"""
from mutators.bufferoverflow_mutator import BufOverflowMutator
from mutators.duplicate_mutator import DuplicateMutator
from mutators.integeroverflow_mutator import IntOverflowMutator
import time  #TODO: remove
import sys


class InfiniteMutator():
    """
    mutator = Mutator("some_strings")
    mutated_str = mutator.mutate()
    """
    def __init__(self, input_str: str = ""):
        self.init_mutators()
        self.set_input_str(input_str)
        self.timers = [0] * 3  #TODO: remove

    def init_mutators(self) -> None:
        buf_overflow = BufOverflowMutator()
        int_overflow = IntOverflowMutator()
        dup = DuplicateMutator()
        self.mutators = [int_overflow, buf_overflow, dup]

    def ordered_mutate(self, stop=10):
        """
        Use this for measuring and debugging
        """
        count = 0
        for index, mutator in enumerate(self.mutators):
            start = time.time()  # TODO: remove
            print(f'starting {type(mutator)}')
            for mutated_data in mutator.mutate():
                print(mutated_data)
                yield mutated_data
            #print(f'{type(mutator)} took {time.time() - start}s')
            self.timers[index] += time.time() - start
            #print(f'{type(mutator)} total {self.timers[index]}')

    def mutate(self):
        """
        A Generator that feeds on a round robin of mutators
        """
        generators = [mutator.mutate() for mutator in self.mutators]
        while len(generators) > 0:
            for index, generator in enumerate(generators):
                mutated_data = next(generator, None)
                if mutated_data is None:
                    generators.pop(index)
                    continue
                yield mutated_data

    def set_input_str(self, input_str: str) -> None:
        """
        Sets input string for each mutator.
        This function also resets all mutator generators.
        """
        self.init_mutators()
        for mutator in self.mutators:
            mutator.set_input_str(input_str)
