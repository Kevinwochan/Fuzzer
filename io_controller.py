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
import subprocess

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

    def is_csv(self) -> bool:
        """
        Checks whether a file is a valid CSV file (comma-separated)
        """
        with open(self.input_path, "r") as csv_file:
            try:
                dialect = csv.Sniffer().sniff(csv_file.read(1024))
                # Perform various checks on the dialect (e.g., lineseparator,
                # delimiter) to make sure it's sane

                # Don't forget to reset the read position back to the start of
                # the file before reading any entries.
                csv_file.seek(0)
                return dialect.delimiter == ","
            except csv.Error:
                # File appears not to be in CSV format;
                return False

    def init_csv_handler(self) -> None:
        """
        Initialize handler for CSV files
        """
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
                # Seeks to the start
                csv_file.seek(0)
                # Read all raw data
                raw_data = csv_file.read()
                # Remove last blank line if exists
                raw_data = raw_data.rstrip()
                self.handlers.append(CsvHandler(data, raw_data))
            except csv.Error:
                return None

    def is_json(self) -> bool:
        """
        Checks whether a file is a valid JSON file
        """
        with open(self.input_path, "r") as json_file:
            try:
                json.load(json_file)
                # Seeks to the start
                json_file.seek(0)
                return True
            except json.decoder.JSONDecodeError:
                return False

    def init_json_handler(self) -> None:
        """
        Initialize handler for JSON files
        """
        with open(self.input_path, "r") as json_file:
            data = json.load(json_file)
            # Seeks to the start
            json_file.seek(0)
            raw_data = json_file.read()
            # Remove last blank line if exists
            raw_data = raw_data.rstrip()
            self.handlers.append(JsonHandler(data, raw_data))

    def is_xml(self) -> bool:
        """
        Checks whether a file is a valid XML file
        """
        with open(self.input_path, "r") as xml_file:
            try:
                xmltodict.parse(xml_file.read())
                # Seeks to the start
                xml_file.seek(0)
                return True
            except xmltodict.expat.ExpatError:
                return False

    def init_xml_handler(self) -> None:
        """
        Initialize handler for XML files
        """
        with open(self.input_path, 'r') as xml_file:
            data = xmltodict.parse(xml_file.read())
            # Seeks to the start
            xml_file.seek(0)
            raw_data = xml_file.read()
            # Remove last blank line if exists
            raw_data = raw_data.rstrip()
            self.handlers.append(XMLHandler(data, raw_data))

    def init_plaintext_handler(self):
        """
        Initialize handler for plaintext files
        """
        with open(self.input_path, "r") as text_file:
            data = [data.strip() for data in text_file]
            raw_data = text_file.read()
            raw_data = raw_data.rstrip()
            self.handlers.append(PlaintextHandler(data, raw_data))

    def init_handlers(self) -> None:
        """
        Detects input file type and initialize correct handler
        """
        if self.is_csv():
            self.init_csv_handler()
        elif self.is_json():
            self.init_json_handler()
        elif self.is_xml():
            self.init_xml_handler()
        else:
            self.init_plaintext_handler()

    def get_handlers(self) -> list:
        return self.handlers

    def run(self, input_str: str = "") -> bool:
        try:
            output = subprocess.check_output(
                [self.binary_path],
                input=input_str.encode(),
            )
        except subprocess.CalledProcessError as e:
            if (e.returncode == -11):
                print(e)
                self.report_vuln(input_str)
                return True
            else:
                print(e.returncode)
        return False

    def run2(self, input_str: str = "") -> bool:
        p = process(self.binary_path)
        try:
            log.warn(f"Trying {input_str}")
            p.send(input_str)
        except Exception as e:
            log.error(e)
            return False
        p.proc.stdin.close()

        # Prevents hang by overwriting the default
        # timeout in pwntools.tube
        p.settimeout(0.1)

        status_code = p.poll(block=True)

        # Ignore hangs/timeouts (None) and SIGABRT (-6)
        if status_code and status_code < 0 and status_code != -6:
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
