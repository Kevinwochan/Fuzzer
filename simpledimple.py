
import multiprocessing as mp
import timeit
import threading
from time import sleep
from pwn import *
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
    while result < n:
        if result >= n:
            result = 0
        yield result
        result += 1

def task(gen, screwyou):
    for val in gen:
        if screwyou.run(val):
            print("found")
            return
def ttt():
    for i in range(400):
        p = process("files/json1")
        p.close()

def subp():
    for i in range(400):
        output = subprocess.check_output(
            ["files/json1"],
            input=b"foo",
        )
        #p = subprocess.Popen(["files/json1"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        #retval = p.communicate(input=b"nah")[0]
        
'''
subprocess.check_output(
    ["files/json1"],
    input=b"foo",
)
'''
if __name__ == '__main__':
    processes=[]
    from io_controller import IoController
    screwyou = IoController("files/json1", "files/json1.txt")
    gen = simple_generator(5000)
    tac = timeit.default_timer()
    task(gen, screwyou)
    tic = timeit.default_timer()
    gen = simple_generator(5000)
    inputs = list(gen)
    processes = []

    NUM_PROCS = mp.cpu_count()
    tuc = timeit.default_timer()
    for i in range(0, len(inputs), int(len(inputs)/NUM_PROCS)):
        spl_inputs = inputs[i:i+int(len(inputs)/NUM_PROCS)]
        p = mp.Process(target=task, args=(spl_inputs, screwyou, ))
        processes.append(p)
        p.start()
    for process in processes:
        process.join()

    toc = timeit.default_timer()
    print(f"{tic - tac}")
    print(f"{toc - tuc}")
    '''
    1 core - 10s
    2 core - 5.1s
    4 core - 3 s
    8 core - 2.5s
    '''
    '''
    tpc = timeit.default_timer()
    screwyou = IoController("files/json1", "files/json1.txt")
    tic = timeit.default_timer()
    print("single-process")
    gen = simple_generator(1000)
    print(type(gen))
    task(gen, screwyou)
    tac = timeit.default_timer()
    print("multi-process")
    gen = simple_generator(1000)
    inputs = list(gen)
    processes = []

    NUM_PROCS = mp.cpu_count()//2
    tuc = timeit.default_timer()
    for i in range(0, len(inputs), int(len(inputs)/NUM_PROCS)):
        spl_inputs = inputs[i:i+int(len(inputs)/NUM_PROCS)]
        p = mp.Process(target=task, args=(spl_inputs, screwyou, ))
        processes.append(p)
        p.start()
    for process in processes:
        process.join()
    toc = timeit.default_timer()
    print(f'{tic-tpc}')
    print(f'{tac-tic}')
    print(f'{tuc-tac}')
    print(f'{toc-tuc}')
'''
    '''
    11.418768399977125
    0.0004450000124052167
    1.428117600036785
    '''

'''Traceback (most recent call last):
Traceback (most recent call last):
  File "/usr/lib/python3.8/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
  File "/usr/lib/python3.8/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "simpledimple.py", line 36, in ttt
    process("files/json1")
  File "/usr/lib/python3.8/multiprocessing/process.py", line 313, in _bootstrap
    self.run()
  File "/home/ctf/.local/lib/python3.8/site-packages/pwnlib/tubes/process.py", line 270, in __init__
    stdin, stdout, stderr, master, slave = self._handles(*handles)
  File "/home/ctf/.local/lib/python3.8/site-packages/pwnlib/tubes/process.py", line 614, in _handles
    master, slave = pty.openpty()
  File "/usr/lib/python3.8/pty.py", line 29, in openpty
    master_fd, slave_name = _open_terminal()
  File "/usr/lib/python3.8/pty.py", line 59, in _open_terminal
    raise OSError('out of pty devices')
  File "/usr/lib/python3.8/multiprocessing/process.py", line 108, in run
OSError: out of pty devices
    self._target(*self._args, **self._kwargs)
  File "simpledimple.py", line 36, in ttt
    process("files/json1")
  File "/home/ctf/.local/lib/python3.8/site-packages/pwnlib/tubes/process.py", line 270, in __init__
    stdin, stdout, stderr, master, slave = self._handles(*handles)
  File "/home/ctf/.local/lib/python3.8/site-packages/pwnlib/tubes/process.py", line 614, in _handles
    master, slave = pty.openpty()
  File "/usr/lib/python3.8/pty.py", line 29, in openpty
    master_fd, slave_name = _open_terminal()
  File "/usr/lib/python3.8/pty.py", line 59, in _open_terminal
    raise OSError('out of pty devices')
'''