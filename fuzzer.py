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

class thread_safe_generator():
    def __init__(self, gen):
        self.gen = gen
        self.lock = threading.Lock()

    def __next__(self):
        with self.lock:
            return next(self.gen)

def thread_safe(f):
    def g(*a, **kw):
        return thread_safe_generator(f(*a, **kw))
    return g

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
        '''
        for new_task in gen:
            result = ioController.run(new_task)
            if result:
                break
        '''
        #tac = timeit.default_timer()
        # fuzzer.py files/csv2 files/csv2.txt
        '''
        4 independent process consuming from the same generator
        '''
    elif MULTI == "check_output":
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

    elif MULTI == "Yes":
        print("multi-process list")
        '''
        Processes work best when we divide the total set of tasks
        between each process and then let them run with a subset, this way we avoid
        the overhead of continually stopping and starting processes

        This takes more memory space tho, because we need to evaluate the entire set of tasks
        before we distribute them
        '''
        '''
        Another optimisation 
        '''
        start_multi = timeit.default_timer()
        inputs = list(gen) # evaluate generator (trade memory for runtime performance)
        time_stamp = timeit.default_timer() - start_multi
        NUM_PROCS = 2
        with mp.Pool(processes=NUM_PROCS) as pool:
            for i in range(0, len(inputs), int(len(inputs)/NUM_PROCS)):
                result = pool.apply_async(ioController.run_list, (inputs[i:i+int(len(inputs)/NUM_PROCS)],))
                if result.get():
                    pool.terminate()
                    break
        print(f'time taken: {timeit.default_timer() - start_multi}, list(gen) took {time_stamp}')
    elif MULTI == "Noyes":
        print("multi-process")
        lock = mp.Lock()
        start_multi = timeit.default_timer()
        with mp.Pool(processes=3) as pool:
            while True:
                lock.acquire()
                new_task = next(gen)
                lock.release()
                if new_task is not None:
                    result = pool.apply_async(ioController.run, (new_task,))
                    if result.get():
                        pool.terminate()
                        break
        print(f'time taken: {timeit.default_timer() - start_multi}')
    else:
        print('uwu bad code, sad man')


''' 
def use_multiprocessing_with_queue2():
    queue = multiprocessing.JoinableQueue()
    num_consumers = multiprocessing.cpu_count() * 2
    results_queue = multiprocessing.Queue()

    for article in Article.objects.all()[5:8]:
        queue.put(article)

    for _ in range(num_consumers):
        p = multiprocessing.Process(target=save_article_result_with_queue2,
                                    args=(queue, results_queue))
        p.start()

    queue.join()

    results = []

    while 1:
        try:
            updated_article = results_queue.get(timeout=1)
        except Empty:
            break
        results.append(updated_article)
    print len(results) 
'''
'''
Generator -> process (sends data to binary) -> process updates the global isDone
          -> process 
'''