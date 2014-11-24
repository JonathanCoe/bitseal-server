#!/bin/bash

ps aux | grep -i bitmessagemain.py | awk {'print $2'} | xargs kill -2
sleep 30 #Give PyBitmessage a reasonable amount of time to shut down gracefully

cd ~/apps/bitseal-server/src
if [ -f nohup.out ];
then
   rm nohup.out
fi

# Before we try to restart PyBitmessage, check whether it is still running (perhaps doing cleanup)
ps cax | grep python > /dev/null
if [ $? -eq 0 ]; then
  # If PyBitmessage  is still running, give it another 30 seconds
  sleep 30 
else
  nohup python bitmessagemain.py >> ~/apps/bitseal-server/src/nohup.out 2>&1 &
  exit
fi

# Check again whether it is safe to restart PyBitmessage
ps cax | grep python > /dev/null
if [ $? -eq 0 ]; then
  # If PyBitmessage  is still running, give it another 30 seconds
  sleep 30
else
  nohup python bitmessagemain.py >> ~/apps/bitseal-server/src/nohup.out 2>&1 &
  exit
fi

# If PyBitmessage has still not closed properly, force kill and restart it
ps cax | grep python > /dev/null
if [ $? -eq 0 ]; then
  ps aux | grep -i bitmessagemain.py | awk {'print $2'} | xargs kill -9
  sleep 10
fi
nohup python bitmessagemain.py >> ~/apps/bitseal-server/src/nohup.out 2>&1 &
exit
