#!/bin/bash

PID_FILE="/tmp/lanmonitor_client.pid"
PYTHON=`which python`

if [ -f $PID_FILE ]; then
    kill -9 `cat $PID_FILE` || exit
fi

$PYTHON ./client.py &
echo $! >$PID_FILE
