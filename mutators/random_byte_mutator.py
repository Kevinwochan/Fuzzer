import random
from pwn import *
from mutators.base_mutator import BaseMutator


class RandomByteMutator(BaseMutator):
    def __init__(self, input_str: str = ""):
        super().__init__(input_str)
    
    def _byte_flip(self) -> str:
        byte_array = bytearray(self.input_str, "UTF-8")
        for i in range(0, len(byte_array)):
            if random.randint(0, 20) == 1:
                byte_array[i] ^= random.getrandbits(7)
        return byte_array.decode("ascii")

    def mutate(self) -> str:
        for i in range(100):
            yield self._byte_flip()
