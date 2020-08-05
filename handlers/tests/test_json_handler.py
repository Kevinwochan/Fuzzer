import unittest
from handlers.json_handler import JsonHandler
from mutators.base_mutator import BaseMutator


class BadMutator(BaseMutator):
    def __init__(self, input_str: str = ""):
        super().__init__(input_str)

    def mutate(self) -> str:
        yield "A"
        return


class JsonHandlerTests(unittest.TestCase):
    """
    Test JsonHandler methods
    """

    def setUp(self):
        self.test_data_dict = {
            "len": 12, "input": "AAAABBBBCCCC", "more_data": ["a", "bb"]}
        self.test_data_raw = '{\n    "len": 12,\n    "input": "AAAABBBBCCCC",\n    "more_data": [\n        "a",\n        "bb"\n    ]\n}'
        self.handler = JsonHandler(
            data_dict=self.test_data_dict,
            data_raw=self.test_data_raw
        )
        mutators = BadMutator()
        self.handler.mutators = mutators

    def test_mutate_elem(self):
        """
        Tests that a primitive is correctly mutated
        """
        self.assertEqual(list(self.handler.mutate_elem("1")), ["A"])
