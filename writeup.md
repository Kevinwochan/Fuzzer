# COMP6447 20T2 Major Project

| Kevin Chan | Kevin Yu | Adam Stucci | Le Pham  | Franklin Wu |
| ---------- | -------- | ----------- | -------- | ----------- |
| z5113136   | z5117900 | z5157372    | z5162043 | z5162043    |


In order to run our fuzzer, the current terminal command is "python3 fuzzer.py <binary file path> <input text file path>"

How does our Fuzzer work:
-------------------------------------------------------------------------------------------------------
The user runs fuzzer.py with binary and text file arguments. The arguments are then processed in the IO Controller which analyses the provided the text file to determine what input format the binary expects.
Sample input file -> fuzzer.py -> IO Controller ->  binary

The IO Controller then parses the text file through the handler for its input format type (e.g CSV, JSON, XML, Plaintext). The handler then mutates the original input format and create new variations of the string that incorporates exploits like buffer overflow, format string exploit, integer overflow/underflow and random byte flips in order to discover potential vulnerabilities in the binary. The altered inputs are then sent back to the IO Controller and ran against the binary and thus the mutator will continue to provide altered inputs until a vulnerability is found or all variations implemented have been used.
IO Controller -> handler -> mutator -> handler -> IO Controller

**IO Controller**

Our IO controller handles the communication between the fuzzer program and the binary.
 Based on the handlers found to be valid for the given sample input file,  The IO controller requests mutations from the handlers which are sent to new processes launched by pwntools.

**Handlers (base_handler.py, csv_handler.py, json_handler.py, xml_handler.py, dict_handler.py, plaintext_handler.py)-**

The handler parses the input text file into a python data structure. The handler may call mutator on different parts of the string such as mutate the whole input or mutate every "field" in the input. The mutated input is then passed up to the IO controller which will then be tested against the binary for vulnerabilities.

Handlers are used as different input formats may need to be processed differently from each other. In our IO Controller, we process the inputs for XML and JSON using xmltodict and json.load which converts the contents of a file into a dictionary of values while CSV and Plaintext converts the contents of the file into a list with different separators like comma or newline. As the dictionary structure of XML and JSON are very similar, the contents are processed through a separate handler called dict_handler.

**Mutators (base_mutator.py, super_mutator.py, bufferoverflow_mutator.py, random_byte_mutator.py, formatstring_mutator.py, integeroverflow_mutator.py)**

When the handler provides the input , the mutator will then alter the string with an exploit we have defined.

- Buffer Overflow exploit:
  Appends up to 1024
  - large random strings
  - newlines
  - cyclic characters
  - duplicated given field/input
  into given input/field. This will ensure that our
- Random bytes exploit:
  - Randomly flips bytes in order to malform parsers to contain non-ascii or special characters.
- Format string mutator:
  - inserts format string characters including "%x", "%s", "%p", and "%n"
- Integer overflow/underflow exploit:
  - replaces string/input with MAX and MIN signed integer value.
??????????????????? Check if we should do this ??????????????????????
  - ?? replaces with largest unsigned integer value ??

If an error is triggered by the binary as a result of our mutated string, it is most likely that a vulnerability has been found as a result of an exploit technique.




What kind of bugs can our fuzzer find:
-------------------------------------------------------------------------------------------------------
As of the mid project write up, we were able to trigger segmentation fault errors on certain binary files using exploits we have learnt throughout the course so far. As a result, the segmentation fault errors may indicate vulnerabilities in the binary as they may be triggered from the use of buffer overflows.


??????????????? It is insufficient if the document merely states "our fuzzer injects random values and finds bugs". We want details that show deep understanding. ??????????????????? Is this good enough?

We have found the following bugs:

CSV1 - Buffer Overflow - segmentation fault was triggered if the input is injected with too many rows which may have overflowed the buffer storing that input, thus overwriting important values in the registers on the stack and causing a crash in the program.

CSV2 - Randomy Byte flip - segmentation fault was triggered after flipping random bytes from the original input in the string and sending it to the binary. This may have resulted in sending characters in which the binary is unable to read which then crashed the program such as inserting non-ascii or special characters like commas.

JSON1 - Buffer Oveflow - segmentation fault was triggerred when overflowing the "len" attribute with 642 bytes which may have overflowed the buffer storing that input, thus overwriting important values in the registers on the stack and causing a crash in the program.

JSON2 -  Buffer Overflow - segementation fault triggered when appending more than 10 duplicate lines of the string given in the text file which may have overflowed the buffer storing that input, thus overwriting important values in the registers on the stack and causing a crash in the program.

XML1 - Format string exploit - segmentation fault when "%s" was appended into one of the website fields (https://google.comAAAAAA%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s). This may be because the "%s" will read for values until an EOF is given, and thus a corruption occurs when the string is processed by the binary.

XML2 - Buffer Overflow - segementation fault when large strings with cyclic characters were inserted into every field given in the input text file which may have overflowed the buffer storing that input, thus overwriting important values in the registers on the stack and causing a crash in the program.

XML3 - Buffer Overflow - ????? TODO: our fuzzer doesn't find this yet ????? - segmentation fault when more than 1 million lines were sent to the binary which may have overflowed the buffer storing that input, thus overwriting important values in the registers on the stack and causing a crash in the program.

Plaintext1 - Buffer Overflow - segmentation fault when any character was appended onto the original input which may have overflowed the buffer storing that input, thus overwriting important values in the registers on the stack and causing a crash in the program.

Plaintext2 - Integer Overflow - ????? TODO: our fuzzer doesn't find this yet ?????? - 

Plaintext3 - Random Byte flip - segmentation fault was triggered after flipping random bytes after "JPG" characters. This may have resulted in sending characters in which the binary is unable to read which then crashed the program such as inserting non-ascii or special characters.

Improvements/Reflection:
-------------------------------------------------------------------------------------------------------
Due to the amount of variations and mutated inputs we want to test, it took exceedingly long to identify vulnerabilities for some binaries despite it being a simple exploit on a particular field. Furthermore, testing buffer overflows were more time consuming than the other exploits as other exploits are specific in what triggers the vulnerability while buffer overflows may require some bruteforce. However, the variations generated by the mutators were essential to thoroughly find potential vulnerabilities and thus all redundant variations were already removed from being tested against the binary for example, we initially had a buffer overflow variation where the string was mutated to include delimiters like special characters. However, this was increasing our search time while also being redundant as Random Byte Flip were triggering the same vulnerabilities in less time and thus the delimiters were removed due to redundancy.

Another improvement we could've strived for was to make our fuzzer more user friendly and practical. While we may have found our vulnerabilities, we wanted to be able to identify what exact exploit was used to identify the vulnerability. For example, Plaintext1 vulnerability was a buffer overflow however any exploit could've been used to malform the original input, as long as it appended extra characters to the original string input. However, this would require us to run the binary against all our exploit variations which is too time consuming to be completed within 180 seconds and therefore comes back to the problem with speed.

We wanted to improve our speed of finding vulnerabilities using
- Multithreading
- Round Robin

?? Talk about improvements in these areas??

Something Awesome:
-------------------------------------------------------------------------------------------------------

**Multiprocessing**
????? NOT FINAL 
- We began with understanding the principles of parallelism and distributing work given a known fixed total work (i.e. `sleep(0.1)` 100000 times) to validate the approach
- When implementing it into fuzzer itself, we found it was no more performant than the single threaded single process implementation we originally had
- Using `python -m cProfile -s time fuzzer.py ...` gave us performance metrics and insights into where our current bottle necks were
- We identified that using pwntools wasn't as performant as expected due to extensive locking issues (specificially blocked by `lock.acquire`, and the issue scaled proportionately with the number of parallel processes) when spawning the binary with multiple processes
- We experimented with a few other process spawning libraries until we found `subprocess.check_output()`, which atomically ran the binary with piped input and returned output and/or any errors!
-----INSERT NUMBERS FOR PERF IMPROV-----
?????

???
