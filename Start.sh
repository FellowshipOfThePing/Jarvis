#!/bin/bash

# Run this file to start both UI and Jarvis assistant. Remember alias 'Jarvis'.

source activate mirror_env


python smartmirror.py &
python Jarvis.py &



