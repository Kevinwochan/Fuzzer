from pwn import *
from mutators.base_mutator import BaseMutator


class BufOverflowMutator(BaseMutator):
    def __init__(self, input_str: str = ""):
        super().__init__(input_str)
    
    def mutate(self) -> str:
        """
        Can be a generator:
        mutator = Mutator("some_strings")
        for mutated_str in mutator.mutate():
            do_stuff(mutated_str)
        """
        #fill one column with  input with all As to trigger buffer overflow or canary
        classic = self.input_str + ("A" * 0x500)
        yield classic
        #fill one column with input with all numbers to trigger buffer overflow or canary
        int_classic = self.input_str + ("1234" * 0x500)
        yield int_classic
        #fill one column with new lines
        byte_str = self.input_str.encode("utf_8")
        newlines = byte_str + (b"\x0a" * 0x500)
        newlines = newlines.decode("utf_8")
        yield newlines
        #create more columns
        test = self.input_str
        for i in range(0x500):
            test +=",test"
        yield test
        # #create more rows
        # test_row = self.input_str
        # for i in range(0x500):
        #     test_row += "\n 1,2,3,4,5,6,7,8,9,0"
        # yield test_row
