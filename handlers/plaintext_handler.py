from handlers.base_handler import BaseHandler
from mutators.bufferoverflow_mutator import BufOverflowMutator
from mutators.formatstring_mutator import FormatStringMutator
from mutators.random_byte_mutator import RandomByteMutator


class PlaintextHandler(BaseHandler):
    """
    Handler for Plaintext file/input.
    """

    def __init__(self, data_raw: str):
        super().__init__(data_raw)

    def generate_input(self) -> str:
        """
        Generate mutated strings from the initial input file.
        """
        buf_overflow = BufOverflowMutator()
        fmt_str = FormatStringMutator()
        rand_byte = RandomByteMutator()
        mutators = [buf_overflow, fmt_str, rand_byte]

        # Pass data through mutators
        for mutator in mutators:
            # Mutate raw data
            mutator.set_input_str(self.data_raw)
            for mutated_str in mutator.mutate():
                yield mutated_str
