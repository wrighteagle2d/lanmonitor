#!/bin/bash

export LANG="POSIC"

PID_FILE="/tmp/lanmonitor_client.pid"
PYTHON=`which python`

if [ -f $PID_FILE ]; then
    kill -9 `cat $PID_FILE` || exit
fi

cd /usr/local/bin/lanmonitor/client

$PYTHON ./client.py &
echo $! >$PID_FILE
