# fuzzer

## COMP6447 Fuzzer Major Project

Run `python3 fuzzer.py program sampleinput.txt` to run fuzzer.

Run `python3 -m unittest` to run unit tests.

Run `python3 fuzzer program sampleinput.txt` to run fuzzer.

Run `python3 utils/adam.py` to run fuzzer against multiple binaries.
Examples:
```
python3 utils/adam.p
python3 utils/adam.p --bins csv*  # will run the fuzzer against all csv files
python3 utils/adam.p --bins 1     # will run the fuzzer against all binaries with a 1
python3 utils/adam.p --bins csv1 json1 # will run the fuzzer against csv1 and json1
```


## Installation

```shell
sudo apt install python3-pip
pip3 install -r requirements.txt
```

## Development

```shell
pip3 install -r requirements-dev.txt
```

### To run tests

```shell
pytest
```

### Compile to binary

#### Install dependencies

```shell
sudo apt-get install python3-dev
sudo apt-get install cython3
```

#### Compile

```shell
cython3 --embed -o fuzzer.c fuzzer.py
gcc -Os -I /usr/include/python3.8 -o fuzzer fuzzer.c -lpython3.8 -lpthread -lm -lutil -ldl
```

#### Run the binary

```shell
./fuzzer program sampleinput.txt
```

### Assumption

- All binaries will have a vulnerability.
- All binaries will function normally (return 0, not crash, no errors) when the relevant input.txt is passed into them.
- All binaries will expect input in one of the following formats:
  - plaintext (multiline)
  - json
  - xml
  - csv
- The input. txt provided will be a valid form of one of these text formats.
- You're fuzzer will have a maximum of 180 seconds per binary to find a vulnerability.
- All binaries will be 32 bit linux ELF's.
- All vulnerabilities will result in memory corruption.

### Hints

- Try sending some known sample inputs (nothing, certain numbers, certain strings, etc)
- Try parsing the format of the input (normal text, json, etc) and send correctly formatted data with fuzzed fields.
- Try manipulating the sample input (bit flips, number replacement, etc)
- Try something awesome :D (There are no right answers)

### Assignment Check-in (10 marks)

- (6 marks) Find a vulnerability in the csv1 and json1 binaries.
- (4 marks) Half page description of your fuzzer functionality so far and the fuzzer design.
- Attempts to make a trivial fuzzer that simply return results from manual source code auditing or relies extensively on other tooling will be considered as not completing the assignment. This will receive a 0 grade

```askii
Initial Diagram for midway submission                              isDone?

            json                      +------------------------+
            +------------------------>|        json            +--------------+
            |               +-------->|       handler          |    no        |
            |               |         |                        |              |
            |               |         +------+-----------------+              |
            |               |          yes   |           ^                    |
            |               |                |           |                    |
            |               |                |           |                    |
            |               |                |           |                    |
            |               |                |           |                    |
            |               |                |           |                    |
            |               |                |           |                    |
            |               +                |           |                    v
            |           +--------+           |           |                +---+---+
            +           |        |           |           +---------------+|      +| overflow
        +------+        |        |   <-------+                            |       |
        |      |        |        |                                        |      +| /dev/random
input   |      |        |        |                                        |       |
type    |      |        |  I/O   |                                        |mutator|
resolver|      |        |        |                                        |       |
        |      |        |        |                                        |      +| spc_char
        +------+        |        |   <------+                             |       |
            +           |        |          |            +---------------+|      +| fmt_str
            |           +--------+          |            |                +---+---+
            |               +               |            |                    ^
            |               |               |            |                    |
            |               |               |            |                    |
            |               |               |            |                    |
            |               |           yes |            |                    |
            |               |               +            v                    |
            |               |         +------------------------+              |
            |               |         |        csv             |              |
            |               +-------->|       handler          +--------------+
            +------------------------>|                        |     no
            csv                      +------------------------+

                                                                isDone?
```
