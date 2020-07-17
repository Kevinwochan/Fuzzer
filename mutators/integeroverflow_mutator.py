from mutators.base_mutator import BaseMutator


class IntOverflowMutator(BaseMutator):
    def __init__(self, input_data=""):
        super().__init__(input_data)

    def mutate(self, step=2, start=1) -> str:
        """
        Return out-of-bound integers
        """
        # Test negative number
        while start <= 0xFFFFFFFFF:
            start = start**2
            yield start
            start *= -1
            yield start
