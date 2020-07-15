from pwn import *
from mutators.base_mutator import BaseMutator


class IntOverflowMutator(BaseMutator):
    def __init__(self, input_str: str = ""):
        super().__init__(input_str)
    
    def mutate(self) -> str:
        """
        Can be a generator:
        mutator = Mutator("some_strings")
        for mutated_str in mutator.mutate():
            do_stuff(mutated_str)
        """
        #Test negative number
        classic = self.input_str + ("-1000")
        yield classic
        # #Test unsigned int
        # 0xFFFFFFF4
        # int_classic = self.input_str + ()
        # yield int_classic