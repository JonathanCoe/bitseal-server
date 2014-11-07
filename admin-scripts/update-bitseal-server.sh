#!/bin/bash

ps aux | grep -i bitmessagemain.py | awk {'print $2'} | xargs kill -2
sleep 10 #Give PyBitmessage a reasonable amount of time to shut down gracefully

# If PyBitmessage  is still running, give it another 30 seconds
ps cax | grep python > /dev/null
if [ $? -eq 0 ]; then
  sleep 30
fi

# If PyBitmessage  is still running, give it another 30 seconds
ps cax | grep python > /dev/null
if [ $? -eq 0 ]; then
  sleep 30
fi

# If PyBitmessage has still not closed properly, force kill it
ps cax | grep python > /dev/null
if [ $? -eq 0 ]; then
  ps aux | grep -i bitmessagemain.py | awk {'print $2'} | xargs kill -9
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

git pull
sleep 10

cd src
nohup python bitmessagemain.py >> ~/apps/bitseal-server/src/nohup.out 2>&1 &
