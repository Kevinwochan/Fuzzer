#!/usr/bin/python3

import os
import sys

from pwn import process, log
from handlers.csv_handler import CsvHandler


if __name__ == "__main__":
    BINARY = sys.argv[1]
    FILENAME = sys.argv[2]
    # TODO: handle arguments for output directory
    OUTPUT = "output/"
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    log.info(f"Binary: {BINARY}")
    log.info(f"Input: {FILENAME}")

    # TODO: handle different inputs
    csvhandler = CsvHandler(FILENAME)

    vuln_count = 0
    for input_str in csvhandler.generate_input():
        p = process(BINARY)
        p.send(input_str)
        p.proc.stdin.close()

        log.warn(f"Trying {input_str}")

        if p.poll(block=True) != 0:
            log.info(f"Found vulnerability!")
            vuln_count += 1
            # TODO: log vuln findings
            with open(f"{OUTPUT}/{vuln_count}", "w") as f:
                f.write(input_str)
                exit()

        p.close()
