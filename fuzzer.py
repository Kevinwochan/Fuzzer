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

def task(gen):
    for _ in range(1000000):
        global isDone
        if isDone:
            break
        val = next(gen)
        if ioController.run(val):
            toc = timeit.default_timer()
            print(f'{toc-tac}')  
            isDone = True
            break

if __name__ == "__main__":
    BINARY = sys.argv[1]
    FILENAME = sys.argv[2]
    tic = timeit.default_timer()

    ioController = IoController(BINARY, FILENAME)
    handlers = ioController.get_handlers()

    isDone = mp.Value('i', 0)

    '''print("normal")
    tac = timeit.default_timer()
    for handler in handlers:
        gen = handler.generate_input()
        task(gen)'''
    '''
    print("multi-thread")
    tac = timeit.default_timer()
    for handler in handlers:
        gen = handler.generate_input()
        pool = mpp.ThreadPool(4)
        for _ in range(10):
            pool.apply_async(task, (gen,))
        pool.close()
        pool.join()
    ioController = IoController(BINARY, FILENAME)
    handlers = ioController.get_handlers()
    '''
    print("multi-process")
    tac = timeit.default_timer()
    # fuzzer.py files/csv2 files/csv2.txt
    csv_handler = handlers[0]
    gen = csv_handler.generate_input()
    
    '''
    4 independent process consuming from the same generator
    '''
    #for mutated_data in gen:
    #    print(mutated_data)
    start = timeit.default_timer()
    with mp.Pool(processes=4) as pool:
        while True:
            new_task = next(gen)
            if new_task is not None:
                result = pool.apply_async(ioController.run, (new_task,))
                if result.get():
                    pool.terminate()
    print(f'time taken: {timeit.default_timer() - start}')


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