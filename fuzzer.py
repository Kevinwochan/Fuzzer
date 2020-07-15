#!/usr/bin/python3

import sys
import os

from pwn import *
from handlers.csv_handler import CsvHandler

'''
Project plan
1. Find vuln from csv1, json1
2. write half page summary

write simple tests for each class

Function breakdown:
- Determines the format of the sample input
    - input: filename
    - return: 'json', 'csv', 'txt'

- parse sample input
    - input: filename of sample input
    - return: a list of byte positions in the sample input byte array

    class position():
        offset
        length

- creates a input formatter
    - input: a list of byte positions to insert payloads
    - return: byte array




- special charactor mutator

- Format string mutator

- Overflow mutator
    - python generator
    - input: string
    - return:

'''

'''
Questions:
    - How to detect segfaults/errors?
    - for complex programs, how are we gonna track state?
        - maybe build a graph?

QUestions for Nhat,
    - Is it okay to 
    - 
'''

'''
TODO: add argparser
'''


'''
Test Suite
'''

'''
BUFFER OVERFLOWS
    http://docs.pwntools.com/en/stable/tubes/processes.html

    docs to consider https://docs.pwntools.com/en/stable/elf/corefile.html 
    "For example, if you have a trivial buffer overflow and don’t want to 
    open up a debugger or calculate offsets, you can use a generated core
    dump to extract the relevant information."
'''
MAX_BUFFER_SIZE = 0x100
PAYLOAD = ''
def run_buffer_test(filename):
    print(f'=== Testing for buffer overflows ===')
    for i in range(0, MAX_BUFFER_SIZE, 4):
        PAYLOAD = 'A' * i
        print(f'Testing with a payoad of size: {len(PAYLOAD)} bytes')
        p = remote('plsdonthaq.me', 4004)
        # p = process(filename)
        # process = subprocess.Popen(args)
        # crashed = process.poll()
        # result = status[crashed is None]
        if p.can_recv(10): # wait until process is ready to receive
            p.sendline(BUFFER)
            p.interactive()
            #p.recvuntil('Segmentation Fault', timeout=10) # D


'''
FORMAT STRINGS
'''

'''
RANDOM INPUT
'''

'''
MUTATED INPUT
'''

'''
Assess the state of the program
'''

if __name__ == '__main__':
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
