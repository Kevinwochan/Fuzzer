import copy
from typing import List
from handlers.base_handler import BaseHandler
from mutators.super_mutator import SuperMutator


class PlaintextHandler(BaseHandler):
    """
    Handler for Plaintext file/input.
    """

    def __init__(self, data_list: list, data_raw: str):
        super().__init__(data_raw)
        self._data_list = data_list
        self._mutators = SuperMutator()

    @property
    def data_list(self) -> List[list]:
        return self._data_list

    @data_list.setter
    def set_data_list(self, data_list: List[list]):
        self._data_list = data_list

    @property
    def mutators(self):
        return self._mutators

    @mutators.setter
    def mutators(self, mutators: list):
        self._mutators = mutators

    def format_data_list(self, data: List[list]) -> str:
        """
        Given a list of rows, return original plaintext string.

        Example:
        Input:
        [["this is ,"],["good"]]

        Output:
        this is ,
        good
        """
        output = ""
        output = "\n".join([str(text) for text in data])
        return output

    def generate_input(self) -> str:
        """
        Generate mutated strings from the initial input file.
        """
        # Initialise mutators with samples
        self.mutators.set_input_str(self.data_raw)
        for mutated_str in self.mutators.mutate():
            yield mutated_str

            # Mutate each row
            for row_n, row in enumerate(self.data_list):
                new_data = copy.deepcopy(self.data_list)
                self.mutators.set_input_str(row)
                for mutated_str in self.mutators.mutate():
                    new_data[row_n] = mutated_str
                    yield self.format_data_list(new_data)
