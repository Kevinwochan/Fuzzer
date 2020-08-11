import random
import string
from pwn import cyclic
from mutators.base_mutator import BaseMutator


class BufOverflowMutator(BaseMutator):
    def __init__(self, input_str: str = ""):
        super().__init__(input_str)

    def mutate(self, max_length: int = 1024, step: int = 128) -> str:
        """
        Return buffer overflow payloads up to
        max_length characters
        max_length: maximum length of the payload (default 1024)
        step: increment step (default 128)
        """
        # Append input with random cyclic characters
        for i in range(0, max_length, step):
            classic = self.input_str + cyclic(i).decode("utf-8")
            yield classic

        # Append input with various strings
        for i in range(0, max_length, step):
            strings = self.input_str + "".join(
                random.choice(string.printable) for s in range(i))
            yield strings

        # Append new lines
        for i in range(0, max_length, step):
            byte_str = self.input_str.encode("utf-8")
            newlines = byte_str + (b"\x0a" * i)
            newlines = newlines.decode("utf-8")
            yield newlines
        self.is_empty = True

    def infinite_mutate(self):
        """
        big boi payloads, bad docs tho :/
        """
        # Append input with random cyclic characters
        string_buffer = 'A'
        while True:
            string_buffer = ''.join(string_buffer, string_buffer)
            yield string_buffer
