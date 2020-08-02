import random
from mutators.base_mutator import BaseMutator


class RandomByteMutator(BaseMutator):
    def __init__(self, input_str: str = ""):
        super().__init__(input_str)

    def byte_flip(self, input_str: str = "") -> str:
        """
        Flip random bits in a string
        """
        byte_array = bytearray(self.input_str, "utf-8")
        for i in range(0, len(byte_array)):
            if random.randint(0, 20) == 1:
                byte_array[i] ^= random.getrandbits(7)
        return byte_array.decode("ascii")

    def mutate(self) -> str:
        for i in range(100):
            yield self.byte_flip(self.input_str)
        self.is_empty = True
