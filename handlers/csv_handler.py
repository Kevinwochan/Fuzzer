import copy
from typing import List
from handlers.base_handler import BaseHandler
from mutators.super_mutator import SuperMutator


class CsvHandler(BaseHandler):
    """
    Handler for CSV file/input.
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
        Given a list of csv rows, return a complete csv string.

        Example:
        Input:
        [["this","is","a","header"],["data1","data2","data3","data4"]]

        Output:
        this,is,a,header
        data1,data2,data3,data4
        """
        output = ""
        rows = []
        for cols in data:
            if len(cols) > 0:
                csv_cols = ",".join(str(cols))
                rows.append(csv_cols)
        output = "\n".join(rows)
        return output

    def generate_input(self) -> str:
        """
        Generate mutated strings from the initial input file.
        """
        # Initialise mutators with samples
        self.mutators.set_input_str(self.data_raw)
        for mutated_str in self.mutators.mutate():
            yield mutated_str

        # Mutate each cell
        for row_n, row in enumerate(self.data_list):
            for col_n, col in enumerate(row):
                self.mutators.set_input_str(row[col_n])
                for mutated_str in self.mutators.mutate():
                    data_list_copy = copy.deepcopy(self.data_list)
                    data_list_copy[row_n][col_n] = mutated_str
                    yield self.format_data_list(data_list_copy)
