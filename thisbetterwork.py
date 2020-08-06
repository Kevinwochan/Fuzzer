
# implement a simple generator and add thread-safe support
import multiprocessing.pool as mpp
import multiprocessing as mp
import timeit
import threading
from time import sleep
from io_controller import IoController
import shutil


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

def simple_generator(n):
    result = 0
    while result < n:
        if result >= n:
            result = 0
        yield result
        result += 1

def task(gen,ioc):
    for val in gen:
        #sleep(0.01)
        if ioc.run(val):
            return True



def task_list(l):
    for item in l:
        sleep(0.01)
    return True
        ##if (i == 9000):
        #    print(val)
        #    break
        #if (val == 9000):
        #    print(val)
        #    break
        #print(next(gen))

if __name__ == '__main__':
    '''tic = timeit.default_timer()
    print("single thread")
    ioc = IoController('files/json1', 'files/json1.txt')
    gen = ioc.handlers[0].generate_input()
    print(type(gen))
    task(gen, ioc)
    '''
    '''
    print("multi-threads")
    gen = thread_safe_generator(bm.mutate())
    pool = mpp.ThreadPool(4)
    for _ in range(10):
        pool.apply_async(task, (gen,))
    pool.close()
    pool.join()
    '''
    toc = timeit.default_timer()

    BASE_STR = 'files/json2'
    for i in range(1, 4):
        shutil.copy(f'{BASE_STR}', f'{BASE_STR}_{i}')
        shutil.copy(f'{BASE_STR}.txt', f'{BASE_STR}_{i}.txt')
    print("multi-process")
    ioc1 = IoController('files/json2_1', 'files/json2_1.txt')
    ioc2 = IoController('files/json2_2', 'files/json2_2.txt')
    ioc3 = IoController('files/json2_3', 'files/json2_3.txt')
    ioc4 = IoController('files/json2_4', 'files/json2_4.txt')
    gen = ioc1.handlers[0].generate_input()
    inputs = list(gen)
    #pool = mp.Pool(4)
    processes = []
    NUM_PROCS = 4
    print("fuzzer-multi-pls-bro")
    gen = ioc1.handlers[0].generate_input()
    inputs = list(gen)
    NUM_PROCS = 4
    ioc = [ioc1,ioc2,ioc3,ioc4]
    with mp.Pool(processes=NUM_PROCS) as pool:
        for i in range(0, len(inputs), int(len(inputs)/NUM_PROCS)):
            result = pool.apply_async(ioc[i].run_list, (inputs[i:i+int(len(inputs)/NUM_PROCS)],))
            if result.get():
                pool.terminate()
                break
    tac = timeit.default_timer()
    '''
    seg_size = int(len(inputs)/NUM_PROCS)
    spl_inputs = inputs[:seg_size]
    p = mp.Process(target=task, args=(spl_inputs,ioc1, ))
    processes.append(p)
    p.start()
   
    spl_inputs = inputs[seg_size:2*seg_size]
    p = mp.Process(target=task, args=(spl_inputs,ioc2, ))
    processes.append(p)
    p.start()


    spl_inputs = inputs[2*seg_size:3*seg_size]
    p = mp.Process(target=task, args=(spl_inputs,ioc3, ))
    processes.append(p)
    p.start()

    spl_inputs = inputs[3*seg_size:]
    p = mp.Process(target=task, args=(spl_inputs,ioc4, ))
    processes.append(p)
    p.start()

    for process in processes:
        process.join()
        #pool.apply_async(task, (gen,))
    tuc = timeit.default_timer()
'''
    print(f'plsbro {tac-toc}')
    '''print(f'single process: {toc-tic}')
    print(f'multiprocess: {tuc-tac}')
    '''