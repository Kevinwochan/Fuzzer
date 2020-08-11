# COMP6447 20T2 Major Project

| Kevin Chan | Kevin Yu | Adam Stucci | Le Pham  | Franklin Wu |
| ---------- | -------- | ----------- | -------- | ----------- |
| z5113136   | z5117900 | z5157372    | z5162043 | z5162043    |


In order to run our fuzzer, the current terminal command is "python3 fuzzer.py <binary file path> <input text file path>"

How does our Fuzzer work:
-------------------------------------------------------------------------------------------------------
Our fuzzer is a smart mutation based fuzzer that treats the tested binary as a black box.

Sample input file -> fuzzer.py -> IO controller -> file_handler -> mutator -> file_handler -> IO controller -> binary

**IO Controller**

Our IO controller handles the communication between files and the fuzzer program. It has two main responsibilities:
Parse the sample input file into a python data structure. The IO controller instantiates handlers to break the python data structure into mutable fields.
Send mutated payloads to the binary

**Handlers (base_handler.py, csv_handler.py, json_handler.py, xml_handler.py, dict_handler.py, plaintext_handler.py)-**

Handlers determine the input formats binaries expect and reformat the text file for processing. In our IO Controller, we process the inputs for XML and JSON as dictionaries while CSV and Plaintext as lists.
The handler may call the mutator on different parts of the string such as mutate the whole input or mutate every "field" in the input. The mutated input is then passed up to the IO controller which will then be tested against the binary for vulnerabilities.

**Mutators (base_mutator.py, super_mutator.py, bufferoverflow_mutator.py, random_byte_mutator.py, formatstring_mutator.py, integeroverflow_mutator.py)**

When the handler provides the input , the mutator will then alter the string with an exploit we have defined.

- Buffer Overflow exploit:
  Appends these payloads into the given input/field:
  - large random strings
  - newlines
  - cyclic characters
  - duplicated given field/input
- Random bytes exploit:
  - Randomly flips bytes in order to malform parsers to contain non-ascii or special characters.
- Format string mutator:
  - inserts format string characters including "%x", "%s", "%p", and "%n"
- Integer overflow/underflow exploit:
  - replaces string/input with powers of 2 positive integers up to the largest 64bit integer
  - replaces string/input with powers of 2 negative integers up to the smallest 64bit integer

If an error is triggered by the binary as a result of our mutated string, it is most likely that a vulnerability has been found as a result of an exploit technique.

What kind of bugs can our fuzzer find:
-------------------------------------------------------------------------------------------------------
The following bugs were found:

**Buffer Overflows: CSV1, JSON2, XML2, Plaintext1**
The Buffer Overflow mutators will replace and duplicate parts of the input up to an infinite amount of size (hardware limiting). 

**Integer overflow: JSON1, Plaintext2**
The Integer Overflow mutator will begin by replacing fields in the sample input starting with positive and negative powers of two up to the maximum 64bit number. After these values are exhausted, the mutator will attempt to insert every possible number.

**Format string exploits: XML1**
The format string mutator will replace fields with common format string characters such as “%s” and “%n”. These strings when printed to standard output using printf cause reads/writes to invalid memory addresses causing memory corruption.

**Invalid data input: CSV2, Plaintext3**
The byte flipping mutator will randomly corrupt a small section of the sample input as it will test non-ascii or special characters against the binary.

Improvements:
-------------------------------------------------------------------------------------------------------
The following improvements could have been made given more time:

**Implementing the fuzzer in a low level language**
By using a lower level language we would be able to optimise the program’s memory management and reduces the overhead of a high level language. With a faster program we would be able to test a larger set of payloads against the binary.

**Tracking code coverage**
Our current implementation is a dumb fuzzer that does not take into account the logic of the tested binary, we could integrate our fuzzer with a disassembler like IDA’s API and give our mutations a heuristic to explore unvisited code paths. 

**Infinite payloads**
Our current implementation relies on a finite set of payloads to be divided between parallel processes. This means that we do not test extreme payloads such as large numbers great than 18446744073709551615 or buffer overflows larger than 1GB.

Something Awesome
-------------------------------------------------------------------------------------------------------
**Testing Script**
- The fuzzer has a companion testing script that allows for users to run the fuzzer against a set of binaries and sample input files
- produces a folder called solved containing all malicious inputs that found vulnerabilities
- produces a test report

```
Diagnostic information
----------------------
Linux distribution: Ubuntu 18.04 bionic
Number of available processors: 8
Python version: 3.8.0
GCC version: [GCC 8.3.0]

Binary      Status                   Time
----------  -----------------  ----------
csv1        PASSED!              0.573441
csv2        PASSED!              0.728198
json1       PASSED!              0.525411
json2       PASSED!              0.524256
plaintext1  PASSED!              0.528062
plaintext2  PASSED!              1.6906
plaintext3  PASSED!              1.08261
xml1        PASSED!             13.1352
xml2        PASSED!              5.97595
xml3        PASSED!             205.698
```

**Round Robin Scheduling**
- Each mutator will generate increasingly complex payloads
- The fuzzer uses a round robin scheme for generating payloads ensuring the simplest form of the malicious input is found

**Multiprocessing**
- We began with understanding the principles of parallelism and distributing work given a known fixed total work (i.e. `sleep(0.1)` 100000 times) to validate the approach
- When implementing it into fuzzer itself, we found it was no more performant than the single threaded single process implementation we originally had
- Using `python -m cProfile -s time fuzzer.py ...` gave us performance metrics and insights into where our current bottle necks were
- We identified that using pwntools wasn't as performant as expected due to extensive locking issues (specifically blocked by `lock.acquire`, and the issue scaled proportionately with the number of parallel processes) when spawning the binary with multiple processes
- We experimented with a few other process spawning libraries until we found `subprocess.check_output()`, which atomically ran the binary with piped input and returned output and/or any errors!



