#!/usr/bin/python3

import os
import sys

from pwn import process, log
from io_controller import IoController

if __name__ == "__main__":
    BINARY = sys.argv[1]
    FILENAME = sys.argv[2]

    ioController = IoController(BINARY, FILENAME)
    handlers = ioController.get_handlers()

    if len(handlers) == 0:
        ioController.warn_unhandled_ftype()
        exit()

    for handler in handlers:
        for input_str in handler.generate_input():
            if ioController.run(input_str):
                ioController.report_vuln(input_str)
                exit()
