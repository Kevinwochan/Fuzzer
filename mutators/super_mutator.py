"""
A super mutator that uses all mutators to generate a sequence of increasingly
complex payloads
"""
from mutators.bufferoverflow_mutator import BufOverflowMutator
from mutators.formatstring_mutator import FormatStringMutator
from mutators.random_byte_mutator import RandomByteMutator
from mutators.integeroverflow_mutator import IntOverflowMutator


class SuperMutator():
    """
    mutator = Mutator("some_strings")
    mutated_str = mutator.mutate()
    """

    def __init__(self, input_str: str = ""):
        buf_overflow = BufOverflowMutator()
        fmt_str = FormatStringMutator()
        rand_byte = RandomByteMutator()
        int_overflow = IntOverflowMutator()
        self.mutators = [buf_overflow, fmt_str, rand_byte, int_overflow]
        self.set_input_str(input_str)

    def is_empty(self):
        for mutator in self.mutators:
            if not mutator.is_empty:
                return False
        return True

    def mutate(self):
        """
        A Generator that feeds on a round robin of mutators
        """
        generators = [mutator.mutate() for mutator in self.mutators]
        while not self.is_empty():
            for generator in generators:
                mutated_data = next(generator, None)
                if mutated_data is None:
                    continue
                yield mutated_data

    def set_input_str(self, input_str: str) -> None:
        for mutator in self.mutators:
            mutator.input_str = input_str
