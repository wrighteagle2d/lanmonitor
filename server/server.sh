#!/bin/bash

LOG="log"
PYTHON=`which python`
PID_FILE="/tmp/lanmonitor_server.pid"

if [ -f $PID_FILE ]; then
    kill -9 `cat $PID_FILE` || exit
fi

cd /usr/local/bin/lanmonitor/server

$PYTHON -mSimpleHTTPServer 1>$LOG 2>&1 &
PID1=$!

sleep 1
$PYTHON ./server.py 1>>$LOG 2>&1 &
PID2=$!

echo $PID1 $PID2 >$PID_FILE

