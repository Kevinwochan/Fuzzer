from mutators.base_mutator import BaseMutator


class IntOverflowMutator(BaseMutator):
    '''
    provides large and negative 32-64bit numbers
    '''
    def __init__(self, input_str: str = ""):
        super().__init__(input_str)

    def mutate(self, step=1, start=2**31) -> int:
        """
        Return out-of-bound integers
        """
        value = start
        for _ in range(step, 64):
            yield value*-1    # large negative value
            yield value       # large value
            value = value**2  # same as logical left shift
