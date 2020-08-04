#!/usr/bin/python3
#cython: language_level=3

import multiprocessing
import argparse
import sys, timeit

from io_controller import IoController

if __name__ == "__main__":
    BINARY = sys.argv[1]
    FILENAME = sys.argv[2]
    parser = argparse.ArgumentParser()
    parser.add_argument('binary')
    parser.add_argument('filename')
    feature_parser = parser.add_mutually_exclusive_group(required=False)
    feature_parser.add_argument('--verbose', '-v', dest='verbose', action='store_true')
    parser.set_defaults(verbose=False)
    args = parser.parse_args()

    ioController = IoController(BINARY, FILENAME, args.verbose)
    handlers = ioController.get_handlers()
    tic = timeit.default_timer()
    for handler in handlers:
        with multiprocessing.Pool() as pool:
            pool.map(ioController.run, handler.generate_input())
            if (ioController.input_str != ""):
                ioController.report_time_elapsed(tic, timeit.default_timer())
                exit()
