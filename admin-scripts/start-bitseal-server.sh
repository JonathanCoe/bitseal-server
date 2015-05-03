#!/bin/bash

# Clear bitseal-server's log file
cd ~/apps/bitseal-server/src
if [ -f nohup.out ];
then
   rm nohup.out
fi

# Start bitseal-server
nohup python bitseal-server.py >> ~/apps/bitseal-server/src/nohup.out 2>&1 &
