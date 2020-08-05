
# implement a simple generator and add thread-safe support
import multiprocessing.pool as mpp
import multiprocessing as mp
import timeit
import threading
class thread_safe_generator():
    def __init__(self, gen):
        self.gen = gen
        print(self.gen)
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
    while True:
        if result >= n:
            result = 0
        yield result
        result += 1

def task(gen):
    for _ in range(100000):
        val = next(gen)
        #print(val)
        if (val == 9000):
            print(val)
            break
        #print(next(gen))

if __name__ == '__main__':
    tic = timeit.default_timer()
    print("single thread")
    gen = thread_safe_generator(simple_generator(100000))
    print(type(gen))
    for _ in range(10):
        task(gen)
    toc = timeit.default_timer()

    print("multi-threads")
    gen = thread_safe_generator(simple_generator(100000))
    pool = mpp.ThreadPool(4)
    for _ in range(10):
        pool.apply_async(task, (gen,))
    pool.close()
    pool.join()
    tac = timeit.default_timer()

    print("multi-process")
    gen = thread_safe_generator(simple_generator(100000))
    #pool = mp.Pool(4)
    processes = []
    for _ in range(10):
        p = mp.Process(target=task, args=(gen,))
        processes.append(p)
        p.start()
    for process in processes:
        process.join()
        #pool.apply_async(task, (gen,))
    tuc = timeit.default_timer()
    print(f'{toc-tic}')
    print(f'{tac-toc}')
    print(f'{tuc-tac}')