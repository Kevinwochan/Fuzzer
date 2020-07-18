#!/usr/bin/python3
#cython: language_level=3

import os
import sys

from pwn import process, log
from handlers.csv_handler import CsvHandler
from handlers.json_handler import JsonHandler


def filetype_unhandled_error(filetype: str):
    log.warn(f"{filetype} unsupported")
    exit()


if __name__ == "__main__":
    BINARY = sys.argv[1]
    FILENAME = sys.argv[2]
    # TODO: handle arguments for output directory
    OUTPUT = "output/"
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    log.info(f"Binary: {BINARY}")
    log.info(f"Input: {FILENAME}")

    # TODO: non-trivial input handler
    # rudimentary input handler
    handler = None
    if "csv" in FILENAME:
        handler = CsvHandler(FILENAME)
    elif "json" in FILENAME:
        handler = JsonHandler(FILENAME)
    elif "plaintext" in FILENAME:
        filetype_unhandled_error("plaintext")
    elif "xml" in FILENAME:
        filetype_unhandled_error("xml")
    elif handler is None:
        filetype_unhandled_error(FILENAME)

    vuln_count = 0
    for input_str in handler.generate_input():
        p = process(BINARY)
        try:
            p.send(input_str)
        except:
            continue
        p.proc.stdin.close()
        log.warn(f"Trying {input_str}")

        if p.poll(block=True) != 0:
            log.info("Found vulnerability!")
            vuln_count += 1
            # TODO: log vuln findings
            with open(f"{OUTPUT}/{vuln_count}", "w") as f:
                f.write(input_str)
                exit()
        p.close()
