#!/usr/bin/python3

import logging as log
import csv
import json
import xmltodict
from pwn import process
from handlers.csv_handler import CsvHandler
from handlers.json_handler import JsonHandler
from handlers.xml_handler import XMLHandler
from handlers.plaintext_handler import PlaintextHandler

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

    def test_xml(self):
        with open(self.input_path, "r") as xml_file:
            try:
                data = xmltodict.parse(xml_file.read())
            except xmltodict.expat.ExpatError:
                return
        with open(self.input_path, 'r') as text_file:
            """
            Given a xml file, return its content as a string.
            """
            raw_data = text_file.read()
            # Remove last blank line if exists
            raw_data = raw_data.rstrip()
            self.handlers.append(XMLHandler(data, raw_data))

    # def test_plaintext(self):
    #     with open(self.input_path, "r") as text_file:
    #         raw_data = text_file.read()
    #         raw_data = raw_data.rstrip()
    #         self.handlers.append(PlaintextHandler(raw_data))

    def init_handlers(self) -> list:
        # self.test_json()
        # self.test_csv()
        self.test_xml()
        # self.test_plaintext()

    def get_handlers(self) -> list:
        return self.handlers

    def run(self, input_str: str = "") -> bool:
        p = process(self.binary_path)
        try:
            p.send(input_str)
        except:
            return False
        p.proc.stdin.close()

        log.warn(f"Trying {input_str}")

        if p.poll(block=True) != 0:
            p.close()
            return True
        else:
            p.close()
            return False

    def warn_unhandled_ftype(self) -> None:
        log.warn(f"{self.input_path} unsupported")

    def report_vuln(self, input_str: str = "") -> None:
        log.info("Found vulnerability!")
        with open(f"{OUTPUT}", "w") as f:
            f.write(input_str)

    def report_time_elapsed(self, tic: float, toc: float) -> None:
        log.info(f"Total duration {toc - tic:0.4f} seconds")
'''
test={
    'a' : {
        'b' : [{
            '@name': 'Lichenstein',
            'c' : '1',
            'd': '2'
        },
        {}]
    }
}
xml = xmltodict.unparse(test, pretty=True, full_document=False)
xml='<a>\n\t<b name="Lichenstein">\n\t\t<c>1</c>\n\t\t<d>2</d>\n\t</b>\n\t<b></b>\n</a>'
'''
