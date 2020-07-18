#!/usr/bin/python3

import csv, json
from pwn import *
from handlers.csv_handler import CsvHandler
from handlers.json_handler import JsonHandler

OUTPUT = "bad.txt"

class IoController:
    """
    io = IO(BINARY, FILENAME)
    filetype = io.gettype()
    io.run("input_string")
    """

    def __init__(self, binary_path: str = "", input_path: str = ""):
        self.binary_path = binary_path
        self.input_path = input_path
        log.info(f"Binary: {binary_path}")
        log.info(f"Input: {input_path}")
        self.handlers = []
        self.init_handlers()

    def test_csv(self):
        with open(self.input_path, "r") as csv_file:
            try:
                """
                Given a csv file, return a list of row dictionary.

                Example:
                Input:
                this,is,a,header
                data1,data2,data3,data4

                Output:
                [["this","is","a","header"],["data1","data2","data3","data4"]]
                """
                data = list(csv.reader(csv_file))
                # Remove last blank line if exists
                if data[-1] == [""] or len(data[-1]) == 0:
                    data.pop()
            except csv.Error:
                return
        with open(self.input_path, "r") as text_file:
            """
            Given a csv file, return its content as a string.
            """
            raw_data = text_file.read()
            # Remove last blank line if exists
            raw_data = raw_data.rstrip()
            self.handlers.append(CsvHandler(data, raw_data))
        
    def test_json(self):
        with open(self.input_path, "r") as json_file:
            try:
                data = json.load(json_file)
            except json.decoder.JSONDecodeError:
                return
        with open(self.input_path, 'r') as text_file:
            """
            Given a json file, return its content as a string.
            """
            raw_data = text_file.read()
            # Remove last blank line if exists
            raw_data = raw_data.rstrip()
            self.handlers.append(JsonHandler(data, raw_data))

    def init_handlers(self) -> list:
        self.test_csv()
        self.test_json()

    def get_handlers(self) -> list:
        return self.handlers

    def run(self, input_str: str = "") -> int:
        p = process(self.binary_path)
        p.send(input_str)
        p.proc.stdin.close()

        log.warn(f"Trying {input_str}")

        if p.poll(block=True) != 0:
            p.close()
            return 1
        else:
            p.close()
            return 0

    def warn_unhandled_ftype(self) -> None:
        log.warn(f"{self.input_path} unsupported")

    def report_vuln(self, input_str: str = "") -> None:
        log.info("Found vulnerability!")
        with open(f"{OUTPUT}", "w") as f:
            f.write(input_str)
