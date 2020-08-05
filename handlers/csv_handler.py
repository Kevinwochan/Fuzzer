import csv
import copy
from typing import List
from handlers.base_handler import BaseHandler
from mutators.bufferoverflow_mutator import BufOverflowMutator
from mutators.formatstring_mutator import FormatStringMutator
from mutators.random_byte_mutator import RandomByteMutator

# This @decorator is totally optional, but it is a recommended best practice
try:  # We try to import GrahamDumpleton/wrapt if available
    from wrapt import decorator
except ImportError:  # fallback to the standard, less complete equivalent
    from functools import wraps as decorator


@decorator
def aslist(generator):
    "Function decorator to transform a generator into a list"
    def wrapper(*args, **kwargs):
        return list(generator(*args, **kwargs))
    return wrapper

class CsvHandler(BaseHandler):
    """
    Handler for CSV file/input.
    """

    def __init__(self, data_list: list, data_raw: str):
        super().__init__(data_raw)
        self._data_list = data_list

    @property
    def data_list(self) -> List[list]:
        return self._data_list

    @data_list.setter
    def set_data_list(self, data_list: List[list]):
        self._data_list = data_list

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
                csv_cols = ",".join(cols)
                rows.append(csv_cols)
        output = "\n".join(rows)
        return output

    def generate_input(self):
        """
        Generate mutated strings from the initial input file.
        """
        buf_overflow = BufOverflowMutator()
        fmt_str = FormatStringMutator()
        rand_byte = RandomByteMutator()
        mutators = [buf_overflow, fmt_str, rand_byte]

        # Pass data through mutators
        for mutator in mutators:
            # Mutate raw data
            mutator.set_input_str(self.data_raw)
            for mutated_str in mutator.mutate():
                yield mutated_str

            # Mutate each cell
            for row_n, row in enumerate(self.data_list):
                new_data = copy.deepcopy(self.data_list)
                for col_n in range(len(row)):
                    mutator.set_input_str(row[col_n])
                    for mutated_str in mutator.mutate():
                        new_data[row_n][col_n] = mutated_str
                        yield self.format_data_list(new_data)
