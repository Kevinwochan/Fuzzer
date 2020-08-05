import multiprocessing
import argparse
import sys, timeit
from io_controller import IoController

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

# Example
if __name__ == '__main__':
    import queue, threading
    BINARY = sys.argv[1]
    FILENAME = sys.argv[2]
    ioController = IoController(BINARY, FILENAME)
    def consumer(q):
        processor = Multiprocessor(cpus=4)
        processor.process(ioController.run, q, q.qsize())
        '''for item in genfrom_queue(q):
            multiprocessor(ioController, )
            if ioController.run(item):
                ioController.report_vuln(item)
                print(f"Time elapsed is {timeit.default_timer() - tic}")
                return'''
            #print(f"trying {item}")
        print("done")

    tic = timeit.default_timer()
    in_q = queue.Queue()
    #processor = Multiprocessor(cpus=4)
    #processor.process(ioController.run, MakeIter(handler.generate_input))
    con_thr = threading.Thread(target=consumer,args=(in_q,))
    con_thr.start()
    #con_thr2 = threading.Thread(target=consumer,args=(in_q,))
    #con_thr2.start()

    #sendto_queue(range(100), in_q)
    for handler in ioController.get_handlers():
        sendto_queue(handler.generate_input(), in_q)
    # Now, pipe a bunch of data into the queue