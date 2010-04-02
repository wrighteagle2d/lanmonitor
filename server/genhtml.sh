#!/bin/bash

HTML="index.html"
HEAD="head.html"
TAIL="tail.html"
PATTERN="192.168.*"

TMPFILE=`mktemp`
cat $HEAD >> $TMPFILE
if [ `ls -1 $PATTERN 2>/dev/null | wc -l` -gt 0 ]; then
    for i in $PATTERN; do
        cat $i >> $TMPFILE
    done
fi
cat $TAIL >> $TMPFILE
mv $TMPFILE $HTML
chmod a+r $HTML
find -name "$PATTERN" -mmin +2 -exec rm '{}' \;
