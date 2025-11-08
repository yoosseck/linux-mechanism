#!/usr/bin/python3
import signal
# set up for the process to ignore the SIGINT signal
signal.signal(signal.SIGINT, signal.SIG_IGN)
while True:
    pass