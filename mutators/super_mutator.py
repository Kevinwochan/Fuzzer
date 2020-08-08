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
        self.init_mutators()
        self.set_input_str(input_str)

    def init_mutators(self) -> None:
        buf_overflow = BufOverflowMutator()
        fmt_str = FormatStringMutator()
        rand_byte = RandomByteMutator()
        int_overflow = IntOverflowMutator()
        self.mutators = [fmt_str, rand_byte, int_overflow, buf_overflow ]

    def is_empty(self) -> bool:
        for mutator in self.mutators:
            if not mutator.is_empty:
                return False
        return True

    def mutate(self) -> str:
        """
        Runs mutate() on all mutators.
        """
        for mutator in self.mutators:
            for mutated_str in mutator.mutate():
                yield mutated_str

    def set_input_str(self, input_str: str) -> None:
        """
        Sets input string for each mutator.
        This function also resets all mutator generators.
        """
        self.init_mutators()
        for mutator in self.mutators:
            mutator.set_input_str(input_str)
