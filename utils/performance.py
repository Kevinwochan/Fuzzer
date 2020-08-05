'''
Various functions to summarise performance and efficiency
'''
import sys
sys.path.append('../')

import os
from tabulate import tabulate

from mutators.super_mutator import SuperMutator
from io_controller import IoController


def measure_duplicates():
    test_summary = []
    for filename in sorted(os.listdir('files')):
        if '.txt' in filename:
            continue
        result = []

        ioController = IoController(f'files/{filename}',
                                    f'files/{filename}.txt')
        handlers = ioController.get_handlers()
        unique_strings = {}
        for handler in handlers:
            for input_str in handler.generate_input():
                if input_str in unique_strings:
                    unique_strings[input_str] += 1
                unique_strings[input_str] = 1

        result.append(f'{filename}')
        result.append(f'{len(unique_strings.keys())}')
        result.append(
            f'{sum([unique_strings[key] for key in unique_strings])}')
        result.append(
            f'{max([unique_strings[key] for key in unique_strings])}')
        test_summary.append(result)
    headers = [
        'test_file', 'unique_strings', 'total strings', 'max duplicates'
    ]
    print(tabulate(test_summary, headers=headers))


measure_duplicates()
