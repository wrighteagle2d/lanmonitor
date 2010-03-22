#!/bin/bash

HTML="index.html"
HEAD="head.html"
TAIL="tail.html"
PATTERN="192.168.*"
LOG="log"
PYTHON=`which python`

exec 1>$LOG 2>&1

rm -f $HTML
for i in $PATTERN; do
   rm -f $i
done

$PYTHON -mSimpleHTTPServer &
$PYTHON ./server.py &

while [ 1 ]; do
    TMPFILE=`mktemp`
    cat $HEAD >> $TMPFILE
    if [ `ls -1 $PATTERN 2>/dev/null | wc -l` -gt 0 ]; then
        for i in $PATTERN; do
            cat $i >> $TMPFILE
        done
    fi
    cat $TAIL >> $TMPFILE
    mv $TMPFILE $HTML
    sleep 4
done
