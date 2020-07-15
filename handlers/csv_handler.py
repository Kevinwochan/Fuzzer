import csv
import copy
import io
import re
from typing import List
from handlers.base_handler import BaseHandler
from mutators.base_mutator import BaseMutator
from mutators.bufferoverflow_mutator import BufOverflowMutator
from mutators.formatstring_mutator import FormatStringMutator


class CsvHandler(BaseHandler):
    """
    Handler for CSV file/input.
    """

    def __init__(self, filename: str, mutators: List[BaseMutator]):
        super().__init__(filename, mutators)

    def __parse_to_list(self) -> list:
        """
        Given a csv file, return a list of rows, each row is a list of columns.

        Example:
        Input:
        this,is,a,header
        data1,data2,data3,data4

        Output:
        [["this","is","a","header"],["data1","data2","data3","data4"]]
        """
        with open(self.filename, "r") as csv_file:
            data = list(csv.reader(csv_file))
            return data
        return []

    def __parse_to_raw(self) -> str:
        """
        Given a csv file, return its content as a string.
        """
        with open(self.filename, "r") as txt_file:
            raw_data = txt_file.read()
            # raw_data_stripped = "\n".join(
            #     [ll.rstrip() for ll in raw_data.splitlines() if ll.strip()]
            # )
            # return raw_data_stripped
            return raw_data
        return ""

    def __format_data(self, data: List[list]) -> str:
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
        for cols in data:
            csv_cols = ",".join(cols)
            output += "\n"
            output += csv_cols
        return output

    def generate_input(self) -> str:
        """
        Generate mutated strings from the initial input file.
        """
        buf_overflow = BufOverflowMutator()
        fmt_str = FormatStringMutator()
        mutators = [buf_overflow, fmt_str]

        for mutator in mutators:
            # Mutate raw data
            mutator.set_input_str(self.raw_data)
            for mutated_str in mutator.mutate():
                yield mutated_str

            for row_n, row in enumerate(self.data):
                new_data = copy.deepcopy(self.data)
                for col_n in range(len(row)):
                    mutator.set_input_str(row[col_n])
                    for mutated_str in mutator.mutate():
                        new_data[row_n][col_n] = mutated_str
                        yield self.__join_data(new_data)

            for row_n, row in enumerate(self.data):
                new_data = copy.deepcopy(self.data)
                new_data[row_n].append("asd")
                yield self.__join_data(new_data)
