#!/usr/bin/python3
import os
ret = os.fork()
if ret == 0:
    os.execve("/bin/echo", ["echo", "Generated with the fork() and the execve()"], {})
elif ret > 0:
    print("Generated the echo command")