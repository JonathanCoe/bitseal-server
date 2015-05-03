#!/bin/bash

# Do a graceful shutdown of bitseal-server
ps aux | grep -i bitseal-server.py | awk {'print $2'} | xargs kill -2

#Give bitseal-server a reasonable amount of time to shut down gracefully
sleep 2

# If bitseal-server  is still running, give it some more time to shut down
ps cax | grep python > /dev/null
if [ $? -eq 0 ]; then
  sleep 5
fi

# If bitseal-server  is still running, give it some more time to shut down
ps cax | grep python > /dev/null
if [ $? -eq 0 ]; then
  sleep 5
fi

# If bitseal-server has still not closed properly, force kill it
ps cax | grep python > /dev/null
if [ $? -eq 0 ]; then
  ps aux | grep -i bitseal-server.py | awk {'print $2'} | xargs kill -9
fi

# Delete all compiled .pyc files in src directory
cd ~/apps/bitseal-server/src
rm *.pyc

# If a nohup.out logging file already exists, delete it
if [ -f nohup.out ];
then
   rm nohup.out
fi

# Delete all compiled .pyc files in pyelliptic directory
cd pyelliptic
rm *.pyc
cd ..

# Delete all compiled .pyc files in socks directory
cd socks
rm *.pyc
cd ../..

# Update the source code
git pull
sleep 10

# Restart bitseal-server
cd src
nohup python bitseal-server.py >> ~/apps/bitseal-server/src/nohup.out 2>&1 &
