import multiprocessing
# https://github.com/antoniojkim/Multiprocessor
class Multiprocessor:
    def __init__(self, cpus=4):
        self.cpus = cpus

    def process(self, function, iterable, arg_generator=lambda a, i: (a,)):
        """
        Process the values in the iterable using the function.
        Parameters
        ----------
        function: callable
            the function that the iterable will be called on
        iterable: list-like, array-like
            the list of items to be processed
        arg_generator: callable
            a function that generates the arguments to `function`
            it takes in part of the iterable as well as an index.
            It should return a tuple of value to be unpacked and
            passed into `function`. By default, it just passes
            the iterable part
        """
        pool = multiprocessing.Pool(processes=self.cpus)

        size = len(iterable) // self.cpus + 1
        TASKS = [
            arg_generator(iterable[i : i + size], i)
            for i in range(0, len(iterable), size)
        ]
        return pool.starmap(function, TASKS)

    def __call__(self, *args, **kwargs):
        self.process(*args, **kwargs)

    def set_cpus(self, cpus):
        self.cpus = cpus