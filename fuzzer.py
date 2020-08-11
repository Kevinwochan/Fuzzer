#!/usr/bin/python3
#cython: language_level=3
import multiprocessing
import argparse
import sys, timeit
from io_controller import IoController
from time import sleep

'''
def genfrom_queue(thequeue):
    while True:
        item = thequeue.get()
        if item is StopIteration:
            thequeue.put(StopIteration)
            break
        yield item

def sendto_queue(items, thequeue):
    for item in items:
        thequeue.put(item)
    thequeue.put(StopIteration)
    
def temp_task(q, size):
    sleep(0.1)

def consumer(q):
    processor = Multiprocessor(cpus=4)
    #processor.process(ioController.run, q, q.qsize())
    processor.process(temp_task, q, q.qsize())

# Example
if __name__ == '__main__':
    import queue, threading
    BINARY = sys.argv[1]
    FILENAME = sys.argv[2]
    ioController = IoController(BINARY, FILENAME)


    tic = timeit.default_timer()
    in_q = queue.Queue()
    #processor = Multiprocessor(cpus=4)
    #processor.process(ioController.run, MakeIter(handler.generate_input))
    con_thr = threading.Thread(target=consumer,args=(in_q,))
    con_thr.start()
    #con_thr2 = threading.Thread(target=consumer,args=(in_q,))
    #con_thr2.start()

    sendto_queue(range(100), in_q)
    sleep(10)
    sendto_queue(range(100, 200),in_q)
    #for handler in ioController.get_handlers():
    #    sendto_queue(handler.generate_input(), in_q)
    '''
'''
#isDone = False#...pretty sure doing nothing yay global variables


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

'''
if __name__ == "__main__":
    BINARY = sys.argv[1]
    FILENAME = sys.argv[2]
    #MULTI = sys.argv[3]
    tic = timeit.default_timer()

    ioController = IoController(BINARY, FILENAME)
    ioController.go()
'''
    handlers = ioController.get_handlers()

    if MULTI == "No":
        print("normal")
        start_single = timeit.default_timer()
        for handler in handlers:
            for input_str in handler.generate_input():
                if ioController.run(input_str):
                    ioController.report_vuln(input_str)
                    print(
                        f'time taken: {timeit.default_timer() - start_single}')
                    exit()
    elif MULTI == "Yes":
        print("multi-process checkoutput")
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
'''



# genqueue.py
#
# Generate a sequence of items that put onto a queue
'''
def genfrom_queue(thequeue):
    while True:
        item = thequeue.get()
        if item is StopIteration: 
            break
        yield item

def sendto_queue(items, thequeue):
    for item in items:
        thequeue.put(item)
    thequeue.put(StopIteration)

# Example
if __name__ == '__main__':
    import queue, threading
    def consumer(q):
        for item in genfrom_queue(q):
            print("Consumed", item)
        print("done")

    in_q = queue.Queue()
    con_thr = threading.Thread(target=consumer,args=(in_q,))
    con_thr.start()

    # Now, pipe a bunch of data into the queue
    sendto_queue(range(100), in_q)
'''