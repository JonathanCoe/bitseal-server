#!/bin/bash

#Stop bitseal-server, giving it a reasonable amount of time to shut down gracefully
ps aux | grep -i bitseal-server.py | awk {'print $2'} | xargs kill -2
sleep 5

# If bitseal-server has still not closed properly, force kill it
ps cax | grep python > /dev/null
if [ $? -eq 0 ]; then
  ps aux | grep -i bitseal-server.py | awk {'print $2'} | xargs kill -9
fi
