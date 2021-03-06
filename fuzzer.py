#!/usr/bin/python3
#cython: language_level=3

import os
import sys, timeit
import multiprocessing as mp
import multiprocessing.pool as mpp
from pwn import process, log
from io_controller import IoController
import threading
#isDone = False#...pretty sure doing nothing


def task(gen, ioController, queue):
    tac = timeit.default_timer()
    for val in gen:
        #global isDone
        #if isDone:
        #    break
        if ioController.run(val):
            toc = timeit.default_timer()
            print(f'Process: {toc-tac}')
            print(f'Total: {toc-twac}')
            #isDone = True
            #if task done, signal parent
            queue.put(True)
            break


if __name__ == "__main__":
    BINARY = sys.argv[1]
    FILENAME = sys.argv[2]
    tic = timeit.default_timer()

    ioController = IoController(BINARY, FILENAME)
    handlers = ioController.get_handlers()

    twac = timeit.default_timer()
    for handler in handlers:  #would want to append the different handlers to our initially created processes rather than killing and creating new processes
        gen = handler.generate_input()
        inputs = list(gen)
        processes = []
        NUM_PROCS = mp.cpu_count()
        queue = mp.Queue(2)
        for i in range(0, len(inputs), int(len(inputs) / NUM_PROCS)):
            spl_inputs = inputs[i:i + int(len(inputs) / NUM_PROCS)]
            p = mp.Process(target=task,
                           args=(
                               spl_inputs,
                               ioController,
                               queue,
                           ))
            processes.append(p)
            p.start()
        if queue.get():
            for process in processes:
                if process.is_alive(): process.kill()
                #process.join()
        queue.close()
