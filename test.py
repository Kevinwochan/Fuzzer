#!/usr/bin/python3

import os
import subprocess
from tabulate import tabulate

OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'


test_summary = []

# This script aims to emulate the testing process Adam will use
for filename in os.listdir('files'):
#for filename in ['csv1']:
    if '.txt' in filename:
        continue

    if os.path.exists('bad.txt'):
        os.remove('bad.txt')

    print(f'=== Testing {filename} ===')
    try:
        cmd = f'./fuzzer files/{filename} files/{filename}.txt > /dev/null'
        p = subprocess.run(cmd, timeout=180, shell=True)
    except:
        test_summary.append([WARNING + filename, 'FAILED: timed out'])
        continue

    if not os.path.exists('bad.txt'):
        test_summary.append([FAIL + filename, 'FAILED: vulnerability not found'])
        continue

    cmd = f'cat bad.txt | files/{filename}'
    p = subprocess.run(cmd, timeout=5, shell=True)
    if p.returncode == 0:
        test_summary.append([WARNING + filename, 'FAILED: could not replicate crash'])
        continue

    test_summary.append([OKGREEN + filename, 'PASSED!'])

headers=['Binary', 'Status'] 
print(tabulate(test_summary, headers=headers))
