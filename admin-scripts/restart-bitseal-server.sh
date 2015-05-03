#!/bin/bash

# Do a graceful shutdown of bitseal-server
ps aux | grep -i bitseal-server.py | awk {'print $2'} | xargs kill -2

# Clear bitseal-server's log file
cd ~/apps/bitseal-server/src
if [ -f nohup.out ];
then
   rm nohup.out
fi

#Give bitseal-server a reasonable amount of time to shut down gracefully
sleep 2

# Before we try to restart bitseal-server, check whether it is still running (perhaps doing cleanup)
ps cax | grep python > /dev/null
if [ $? -eq 0 ]; then
  # If bitseal-server  is still running, give it some more time to shut down
  sleep 5 
else
  # If bitseal-server  is no longer running, restart it
  nohup python bitseal-server.py >> ~/apps/bitseal-server/src/nohup.out 2>&1 &
  exit
fi

# Check again whether it is safe to restart bitseal-server
ps cax | grep python > /dev/null
if [ $? -eq 0 ]; then
  # If bitseal-server  is still running, give it some more time to shut down
  sleep 5
else
  # If bitseal-server  is no longer running, restart it
  nohup python bitseal-server.py >> ~/apps/bitseal-server/src/nohup.out 2>&1 &
  exit
fi

# If bitseal-server has still not closed properly, force kill and restart it
ps cax | grep python > /dev/null
if [ $? -eq 0 ]; then
  ps aux | grep -i bitseal-server.py | awk {'print $2'} | xargs kill -9
  sleep 5
fi
nohup python bitseal-server.py >> ~/apps/bitseal-server/src/nohup.out 2>&1 &
exit
