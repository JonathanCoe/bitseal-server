#!/bin/bash

ps aux | grep -i bitmessagemain.py | awk {'print $2'} | xargs kill -2
sleep 60 #Give PyBitmessage a reasonable amount of time to shut down gracefully

# If PyBitmessage  is still running, give it another 60 seconds
ps cax | grep python > /dev/null
if [ $? -eq 0 ]; then
  sleep 60
fi

# If PyBitmessage  is still running, give it another 60 seconds
ps cax | grep python > /dev/null
if [ $? -eq 0 ]; then
  sleep 60
fi

# If PyBitmessage has still not closed properly, force kill it
ps cax | grep python > /dev/null
if [ $? -eq 0 ]; then
  ps aux | grep -i bitmessagemain.py | awk {'print $2'} | xargs kill -9
fi

cd ~/apps/bitseal-server/src
rm *.pyc
if [ -f nohup.out ];
then
   rm nohup.out
fi

cd pyelliptic
rm *.pyc
cd ..

cd socks
rm *.pyc
cd ../..

git pull
sleep 10

cd src
nohup python bitmessagemain.py >> ~/apps/bitseal-server/src/nohup.out 2>&1 &
