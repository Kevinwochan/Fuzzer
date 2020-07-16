#!/usr/bin/python3

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
    if "csv" in FILENAME:
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
    elif "json" in FILENAME:
        jsonhandler = JsonHandler(FILENAME)

        vuln_count = 0
        for input_str in jsonhandler.generate_input():
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
    elif "plaintext" in FILENAME:
        filetype_unhandled_error("plaintext")
    elif "xml" in FILENAME:
        filetype_unhandled_error("xml")


        '''
        Traceback (most recent call last):
  File "fuzzer.py", line 52, in <module>
    p.send(input_str)
  File "/home/ub/.local/lib/python3.6/site-packages/pwnlib/tubes/tube.py", line 743, in send
    data = context._encode(data)
  File "/home/ub/.local/lib/python3.6/site-packages/pwnlib/context/__init__.py", line 831, in _encode
    return s.encode('latin1')
AttributeError: 'list' object has no attribute 'encode
'''