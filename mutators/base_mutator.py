class BaseMutator:
    """
    mutator = Mutator("some_strings")
    mutated_str = mutator.mutate()
    """

    def __init__(self, input_str: str = ""):
        self.input_str = input_str
        self._is_empty = False

    def mutate(self) -> str:
        """
        Can be a generator:
        mutator = Mutator("some_strings")
        for mutated_str in mutator.mutate():
            do_stuff(mutated_str)
        """
        pass

    def set_input_str(self, input_str: str) -> None:
        self.input_str = input_str
        self._is_empty = False

    @property
    def is_empty(self) -> bool:
        """
        If a mutator has run out of payloads
        """
        return self._is_empty

    @is_empty.setter
    def is_empty(self, boolean):
        self._is_empty = boolean
