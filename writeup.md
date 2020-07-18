# COMP6447 20T2 Major Project
-------------------------------------------------------------------------------------------------------

|Kevin Chan | Kevin Yu | Adam Stucci | Le Pham | Franklin Wu|
| ------------- | 
|z5113136 |  z5161477 | z5157372 | z5162043 | z5162043|


Basic Overview:
-------------------------------------------------------------------------------------------------------

In order to run our fuzzer, the current terminal command is:
```
python3 fuzzer.py <binary file path> <input text file path> 
ls bad.txt
bad.txt

```
Our group was tasked to create a fuzzer program which looks for vulnerabilities when given a binary file. We are given binary files to test with in which may require different input formats that include:  CSV, JSON, Plaintext, and XML. Each binary file has a corresponding input text file which outlines the type of format and input the binary expects. 

How our fuzzer works:
-------------------------------------------------------------------------------------------------------
For each binary file, our fuzzer program reads in the corresponding input text file in order to assess the input type and send mutated versions of the initial input in order to trigger the binary to reveal a vulnerability. There are 3 main sections of our fuzzer program:

```
          Initial Diagram for midway submission                              isDone?

                     json                              +------------------------+
                     +-------------------------------->|        json            +--------------+
                     |                       +-------->|       handler          |    no        |
                     |                       |         |                        |              |
                     |                       |         +------+-----------------+              |
                     |                       |          yes   |           ^                    |
                     |                       |                |           |                    |
                     |                       |                |           |                    |
                     |                       |                |           |                    |
                     |                       |                |           |                    |
                     |                       |                |           |                    |
                     |                       |                |           |                    |
                     |                       +                |           |                    v
                     |                   +--------+           |           |                +---+---+
                     +                   |        |           |           +---------------+|      +| overflow
                  +------+               |        |   <-------+                            |       |
                  |      |               |        |                                        |      +| /dev/random
          input   |      |               |        |                                        |       |
          type    |      |               |  I/O   |                                        |mutator|
          resolver|      |               |        |                                        |       |
                  |      |               |        |                                        |      +| spc_char
                  +------+               |        |   <------+                             |       |
                     +                   |        |          |            +---------------+|      +| fmt_str
                     |                   +--------+          |            |                +---+---+
                     |                       +               |            |                    ^
                     |                       |               |            |                    |
                     |                       |               |            |                    |
                     |                       |               |            |                    |
                     |                       |           yes |            |                    |
                     |                       |               +            v                    |
                     |                       |         +------------------------+              |
                     |                       |         |        csv             |              |
                     |                       +-------->|       handler          +--------------+
                     +-------------------------------->|                        |     no
                      csv                              +------------------------+

                                                                          isDone?
```

Determine input type (fuzzer.py)
-------------------------------------------------------------------------------------------------------
As of the mid project write up, our fuzzer program determines the input format of the binary by checking the name of the binary and text file. From the files we are given, the names indicate what text file they expect and hence from that, we are able to choose what handler we want to use.

Handlers Class
-------------------------------------------------------------------------------------------------------
Handlers (base_handler.py, csv_handler.py, json_handler.py)-
Once we determine the input text type, we utilse the matching handler in order to read the input text file. Currently, the handler parses the input text file into a string which is then altered by mutators; the handler may call mutator on different parts of the string such as mutate the whole input or mutate every "cell" in each row given in the input. The handler then sends every generated mutated string to the binary and records the response of the binary. If a vulnerability is detected, the handler will notify the fuzzer which will then return the appropriate notification back to the user.


Mutators Class
-------------------------------------------------------------------------------------------------------
Mutators (base_mutator.py, bufferoverflow_mutator.py, random_byte_mutator.py, formatstring_mutator.py)-
Once the handler provides a string, the mutator will then alter the string with an exploit we have defined. This may involve appending certain characters to the string or changing each character in the string as the altered strings reflect exploits we have learnt throughout the course such as buffer overflow. If an error is triggered by the binary as a result of our mutated string, it is most likely that a vulnerability has been found as a result of an exploit technique.

 
 
What kind of bugs can our fuzzer find as of now:
-------------------------------------------------------------------------------------------------------
As of the mid project write up, we were able to trigger segmentation fault errors on certain binary files using exploits we have learnt throughout the course so far. As a result, the segmentation fault errors may indicate vulnerabilities in the binary as they may be triggered from the use of buffer overflows.
We have found the following bugs:

CSV1 - segmentation fault was triggered if the input is injected with too many rows (buffer overflow)

CSV2 - segmentation fault was triggered after flipping random bytes from the original input in the string and sending it to the binary. This may have resulted in sending characters in which the binary is unable to read which then crashed the program.
