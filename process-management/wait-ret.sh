#!/bin/bash
false &
wait $! # Await the end of the process. The false command's PID is retrieved from the $! variable
echo "The false command is terminated. : $?" # The return value of the false process is retrieved after the wait