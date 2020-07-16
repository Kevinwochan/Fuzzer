class BaseMutator:
    """
    mutator = Mutator("some_strings")
    mutated_str = mutator.mutate()
    """

    def __init__(self, input_str: str = ""):
        self.input_str = input_str

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
