#!/usr/bin/python3

import sys

from pwn import process, log
from handlers.csv_handler import CsvHandler


if __name__ == "__main__":
    BINARY = sys.argv[1]
    FILENAME = sys.argv[2]

    log.info(f"Binary: {BINARY}")
    log.info(f"Input: {FILENAME}")

    # run_buffer_test(FILENAME)
    csvhandler = CsvHandler(FILENAME)
    with open("output.txt", "w") as f:
        for input_str in csvhandler.generate_input():
            p = process(BINARY)
            p.send(input_str)
            p.proc.stdin.close()

            log.warn(f"Trying {input_str}")
            f.write(input_str)

            if p.poll(block=True) != 0:
                log.info(f"Found vulnerability")
                f.write("Found vulnerability")
                exit()

            p.close()
