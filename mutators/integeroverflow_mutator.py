from mutators.base_mutator import BaseMutator


class IntOverflowMutator(BaseMutator):
    '''
    provides large and negative 32-64bit numbers
    '''
    def __init__(self, input_str: str = ""):
        super().__init__(input_str)

    def mutate(self) -> str:
        """
        Return out-of-bound integers
        """
        value = 2
        for _ in range(1, 64):
            yield str(value * -1 + 1)  # large negative value
            yield str(value * -1)  # large negative value
            yield str(value)  # large value
            value = 2 * value  # same as logical left shift
        self.is_empty = True

    def infinite_mutate(self) -> str:
        yield 0
        value = 1
        while True:
            yield value
            yield value * -1
            value += 1
