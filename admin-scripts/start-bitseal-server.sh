#!/bin/bash

cd ~/apps/bitseal-server/src
if [ -f nohup.out ];
then
   rm nohup.out
fi

sleep 5
nohup python bitmessagemain.py >> ~/apps/bitseal-server/src/nohup.out 2>&1 &
