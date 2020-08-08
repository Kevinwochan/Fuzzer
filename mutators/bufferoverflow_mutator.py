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
        # Multiply random lines
        lines = self.input_str.split("\n")
        n_lines = len(lines)
        for i in range(0, max_length, step):
            rand_line_index = random.randint(0, n_lines - 1)
            for j in range(i):
                lines.append(lines[rand_line_index])
            multi_lines = "\n".join(lines)
            yield multi_lines

        # Append input with random cyclic characters
        for i in range(0, max_length, step):
            classic = self.input_str + cyclic(i).decode("utf-8")
            yield classic

        # Append input with various strings
        for i in range(0, max_length, step):
            strings = self.input_str + "".join(
                random.choice(string.printable) for s in range(i)
            )
            yield strings

        # Append new lines
        for i in range(0, max_length, step):
            byte_str = self.input_str.encode("utf-8")
            newlines = byte_str + (b"\x0a" * i)
            newlines = newlines.decode("utf-8")
            yield newlines

        # Append random delimiters and characters
        # delimiters = [
        #     "'",
        #     '"',
        #     ",",
        #     ".",
        #     ";",
        #     "/",
        #     "\\",
        #     "{",
        #     "}",
        #     "[",
        #     "]",
        #     "-",
        #     "=",
        #     "+",
        #     "&",
        #     "?",
        #     "#",
        #     "(",
        #     ")",
        #     "@",
        #     "!",
        # ]
        # for delim in delimiters:
        #     for i in range(0, max_length, step):
        #         delim_str = self.input_str + (
        #             (delim + random.choice(string.ascii_letters)) * i
        #         )
        #         yield delim_str
        # self.is_empty = True
