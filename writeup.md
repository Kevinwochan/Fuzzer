# COMP6447 20T2 Major Project

| Kevin Chan | Kevin Yu | Adam Stucci | Le Pham  | Franklin Wu |
| ---------- | -------- | ----------- | -------- | ----------- |
| z5113136   | z5161477 | z5157372    | z5162043 | z5162043    |


In order to run our fuzzer, the current terminal command is "python3 fuzzer.py <binary file path> <input text file path>"

Basic Overview:
-------------------------------------------------------------------------------------------------------
Sample input file -> fuzzer.py -> IO Controller ->  binary

IO Controller -> handler -> mutator -> handler -> IO Controller

**Mutators (base_mutator.py, bufferoverflow_mutator.py, random_byte_mutator.py, formatstring_mutator.py)**

When the handler provides a string, the mutator will then alter the string with an exploit we have defined.

- Buffer Overflow exploit: appending a large amount of chracters
- Random bytes exploit: randomly flips bytes corruptiung parsers
- Format string mutator: inserts format string characters like "%x"

If an error is triggered by the binary as a result of our mutated string, it is most likely that a vulnerability has been found as a result of an exploit technique.

**Handlers (base_handler.py, csv_handler.py, json_handler.py)-**

The handler parses the input text file into a python data structure. The handler may call mutator on different parts of the string such as mutate the whole input or mutate every "cell" in the input. The mutated input is then passed up to the IO controller.

**IO Controller**

Our IO controller handles the communication between the fuzzer program and the binary.
 Based on the handlers found to be valid for the given sample input file,  The IO controller requests mutations from the handlers which are sent to new processes launched by pwntools. 


What kind of bugs can our fuzzer find as of now:
-------------------------------------------------------------------------------------------------------
As of the mid project write up, we were able to trigger segmentation fault errors on certain binary files using exploits we have learnt throughout the course so far. As a result, the segmentation fault errors may indicate vulnerabilities in the binary as they may be triggered from the use of buffer overflows.
We have found the following bugs:

CSV1 - Buffer Overflow - segmentation fault was triggered if the input is injected with too many rows

CSV2 - segmentation fault was triggered after flipping random bytes from the original input in the string and sending it to the binary. This may have resulted in sending characters in which the binary is unable to read which then crashed the program.

JSON1 - Buffer Oveflow - segmentation fault was triggerred when overflowing the "len" attribute with 642 bytes


Improvements
-------------------------------------------------------------------------------------------------------
- implement multithreading to increase amount of possible attacks
- fuzzer could learn state changes and mutate accordingly
- implement a mutators should be able to generate primitive exploits not just strings