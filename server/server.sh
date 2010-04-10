#!/bin/bash

PYTHON=`which python`
PID_FILE="/tmp/lanmonitor_server.pid"

if [ -f $PID_FILE ]; then
    kill -9 `cat $PID_FILE` || exit
fi

cd /usr/local/bin/lanmonitor/server

$PYTHON ./server.py &
PID=$!

echo $PID >$PID_FILE

