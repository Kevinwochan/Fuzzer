import csv
import copy
import io
import re
import random
from typing import List
from handlers.base_handler import BaseHandler
from mutators.base_mutator import BaseMutator
from mutators.bufferoverflow_mutator import BufOverflowMutator
from mutators.formatstring_mutator import FormatStringMutator
from mutators.random_byte_mutator import RandomByteMutator


class CsvHandler(BaseHandler):
    """
    Handler for CSV file/input.
    """

    def __init__(self, sample_filename: str):
        super().__init__(sample_filename)

    def parse_to_list(self) -> list:
        """
        Given a csv file, return a list of row dictionary.

        Example:
        Input:
        this,is,a,header
        data1,data2,data3,data4

        Output:
        [["this","is","a","header"],["data1","data2","data3","data4"]]
        """
        with open(self.sample_filename, "r") as csv_file:
            data = list(csv.reader(csv_file))
            return data
        return []

    def parse_to_raw(self) -> str:
        """
        Given a csv file, return its content as a string.
        """
        with open(self.sample_filename, "r") as txt_file:
            raw_data = txt_file.read()
            return raw_data
        return ""

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

    def generate_input(self) -> str:
        """
        Generate mutated strings from the initial input file.
        """
        buf_overflow = BufOverflowMutator()
        fmt_str = FormatStringMutator()
        rand_byte = RandomByteMutator()
        mutators = [buf_overflow, fmt_str, rand_byte]

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

        # Append new columns up to 1000 columns
        for row_n, row in enumerate(self.data_list):
            new_data = copy.deepcopy(self.data_list)
            for i in range(1000):
                for j in range(i):
                    new_data[row_n].append("A")
                    yield self.format_data_list(new_data)

        # Duplicate rows up to 1000 rows
        new_data = copy.deepcopy(self.data_list)
        for i in range(1000):
            for j in range(i):
                new_data.append(new_data[random.randint(0, len(new_data) - 1)])
                yield self.format_data_list(new_data)
