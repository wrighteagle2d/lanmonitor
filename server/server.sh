#!/bin/bash

HTML="index.html"
PATTERN="192.168.*"
LOG="log"
PYTHON=`which python`
PID_FILE="/tmp/lanmonitor_server.pid"

if [ -f $PID_FILE ]; then
    kill -9 `cat $PID_FILE` || exit
fi

cd /usr/local/bin/lanmonitor/server

rm -f $HTML
for i in $PATTERN; do
   rm -f $i
done

./genhtml.sh

$PYTHON -mSimpleHTTPServer 1>$LOG 2>&1 &
PID1=$!

sleep 1
$PYTHON ./server.py &
PID2=$!

echo $PID1 $PID2 >$PID_FILE

