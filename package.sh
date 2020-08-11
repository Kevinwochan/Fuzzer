#!/bin/bash
tar -czvf fuzzer.tar fuzzer install.sh requirements.txt generators/ mutators/ handlers/ fuzzer.py io_controller.py utils/

