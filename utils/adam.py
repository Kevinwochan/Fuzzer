#!/usr/bin/python3
'''
This script aims to emulate the testing process Adam will use
'''

import os
import sys
import subprocess
import argparse
import time
import shutil
import distro
import multiprocessing as mp
from tabulate import tabulate

OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDCOLOR = '\x1b[0m'

sys.path.append('../')


def is_selected(filename, selected_bins):
    for selected in selected_bins:
        if selected in filename:
            return True
    return False


parser = argparse.ArgumentParser(
    description=
    'Run with a folder called "files" containing binaries and sample input text files'
)
parser.add_argument('--debug',
                    help='displays the output of the fuzzer program',
                    action='store_true',
                    default=False)
parser.add_argument('--timeout',
                    help='maximum amount of time the fuzzer is allowed to run',
                    default=180)
parser.add_argument(
    '--bins',
    nargs="*",
    help=
    'Explicity name binaries to run this script against (default: all binaries in files)',
    default='')
args = parser.parse_args()

test_summary = []

for filename in sorted(os.listdir('files')):

    if '.txt' in filename:
        continue

    if len(args.bins) > 0 and not is_selected(filename, args.bins):
        continue

    if os.path.exists('bad.txt'):
        os.remove('bad.txt')

    print(f'=== Testing {filename} ===')
    total_time = 0
    try:
        cmd = f'python3 fuzzer.py files/{filename} files/{filename}.txt > /dev/null'
        start = time.time()
        p = subprocess.run(cmd, timeout=int(args.timeout), shell=True)
        total_time = time.time() - start
        print(f'time taken: {total_time}s')
    except:
        total_time = time.time() - start
        print('FAILED: timed out')
        test_summary.append([
            WARNING + filename, 'FAILED: timed out',
            str(total_time) + ENDCOLOR
        ])
        continue

    # Verify bad.txt file output was created
    if not os.path.exists('bad.txt'):
        print('FAILED: vulnerability not found')
        test_summary.append([
            FAIL + filename, 'FAILED: vulnerability not found',
            str(total_time) + ENDCOLOR
        ])
        continue
    # Verify vulnerabilitie produces error code
    shutil.copy('bad.txt', f'solved/{filename}.txt')
    cmd = f'cat bad.txt | files/{filename} > /dev/null'
    if args.debug:
        cmd = f'cat bad.txt | files/{filename}'
    p = subprocess.run(cmd, timeout=5, shell=True)
    if p.returncode == 0:
        print('FAILED: could not replicate crash')
        test_summary.append([
            WARNING + filename, 'FAILED: could not replicate crash',
            str(total_time) + ENDCOLOR
        ])
        continue
    print('PASSED!')
    test_summary.append(
        [OKGREEN + filename, 'PASSED!',
         str(total_time) + ENDCOLOR])

headers = ['Binary', 'Status', 'Time']
TITLE = 'Diagnostic information\n----------------------'
SYS_VER = sys.version.split('\n')
LINUX_VER = 'Linux distribution: ' + ' '.join(distro.linux_distribution())
NUM_PROC = 'Number of available processors: ' + str(mp.cpu_count())
PYTHON_VER = 'Python version: ' + SYS_VER[0].split(' ')[0]
GCC_VER = 'GCC version: ' + SYS_VER[1]
print('\n'.join([TITLE, LINUX_VER, NUM_PROC, PYTHON_VER, GCC_VER]))
print(tabulate(test_summary, headers=headers))
