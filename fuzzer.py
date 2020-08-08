#!/usr/bin/python3
#cython: language_level=3

import os
import sys, timeit
import multiprocessing as mp
import multiprocessing.pool as mpp
from pwn import process, log
from io_controller import IoController
import threading
isDone = False


def task(gen, ioController):
    tac = timeit.default_timer()
    for val in gen:
        global isDone
        if isDone:
            break
        if ioController.run(val):
            toc = timeit.default_timer()
            print(f'Process: {toc-tac}')  
            print(f'Total: {toc-twac}')  
            isDone = True
            break

if __name__ == "__main__":
    BINARY = sys.argv[1]
    FILENAME = sys.argv[2]
    MULTI = sys.argv[3]
    tic = timeit.default_timer()

    ioController = IoController(BINARY, FILENAME)
    handlers = ioController.get_handlers()

    csv_handler = handlers[0]
    gen = csv_handler.generate_input()
    if MULTI == "No":
        print("normal")
        start_single = timeit.default_timer()
        for handler in handlers:
            for input_str in handler.generate_input():
                if ioController.run(input_str):
                    ioController.report_vuln(input_str)
                    print(f'time taken: {timeit.default_timer() - start_single}')
                    exit()
    elif MULTI == "Yes":
        print("multi-process checkoutput")
        twac = timeit.default_timer()
        for handler in handlers:
            gen = handler.generate_input()
            alsdf = timeit.default_timer()
            inputs = list(gen)
            print(f"{timeit.default_timer() - alsdf} sdf")
            processes = []
            NUM_PROCS = mp.cpu_count()
            for i in range(0, len(inputs), int(len(inputs)/NUM_PROCS)):
                spl_inputs = inputs[i:i+int(len(inputs)/NUM_PROCS)]
                p = mp.Process(target=task, args=(spl_inputs, ioController, ))
                processes.append(p)
                p.start()
            for process in processes:
                process.join()
