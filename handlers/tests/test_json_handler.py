import unittest
import tempfile
import json
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
        self.tmp_file = tempfile.NamedTemporaryFile(mode="w")
        self.test_data_dict = {
            "len": 12, "input": "AAAABBBBCCCC", "more_data": ["a", "bb"]}
        self.test_data_raw = '{\n    "len": 12,\n    "input": "AAAABBBBCCCC",\n    "more_data": [\n        "a",\n        "bb"\n    ]\n}'
        # Write test data to temp file
        with open(self.tmp_file.name, "w") as tmp_json:
            json.dump(self.test_data_dict, tmp_json,
                      indent=4)  # indenting matches samples
        self.handler = JsonHandler(sample_filename=self.tmp_file.name)
        mutators = [BadMutator()]
        self.handler.mutators = mutators

    def tearDown(self):
        self.tmp_file.close()

    def test_mutate_elem(self):
        """
        Tests that a primitive is correctly mutated
        """
        self.assertEqual(list(self.handler.mutate_elem("1")), ["A", "1"])

    def test_mutate_structure(self):
        """
        Tests that a JSON is mutated in every field
        """
        mutated_set = (self.handler.mutate_structure(self.test_data_dict))
        self.assertIn({"len": "A", "input": "AAAABBBBCCCC",
                       "more_data": ["a", "bb"]}, mutated_set)
        self.assertIn({"len": 12, "input": "AAAABBBBCCCC",
                       "more_data": ["a", "bb"]}, mutated_set)
        self.assertIn({"len": 12, "input": "AAAABBBBCCCC",
                       "more_data": ["A", "bb"]}, mutated_set)
        self.assertIn({"len": 12, "input": "AAAABBBBCCCC",
                       "more_data": ["a", "A"]}, mutated_set)
