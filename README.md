# fuzzer

## COMP6447 Fuzzer Major Project

Run `python3 fuzzer.py program sampleinput.txt` to run fuzzer.

Run `python3 -m unittest` to run unit tests.

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
