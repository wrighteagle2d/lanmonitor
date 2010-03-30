#!/usr/bin/env python

import os
import sys
import time
import socket

host = '192.168.26.160'
port = 50000

def get_output(cmd):
    pipe = os.popen(cmd)
    output = pipe.read()
    pipe.close()
    return output

def build_message( ):
    message = uptime() + ", "
    message += rcssserver()
    return message 

def uptime() :
    return get_output('uptime').strip()

def testing() :
    return get_output("ps -o comm= -e | sort | uniq -c | sort -nr | head -2 | awk '{print $2}'").strip().split('\n')

def rcssserver() :
    output = get_output('ps -o user= -C rcssserver').split('\n');
    count = len(output) - 1;
    if count > 0:
        team = testing()
        return ' #rcssserver: %d,%s(%s,%s)' % (count, output[0], team[0], team[1])
    return ' #rcssserver: 0'

def communicate(s) :
    while 1:
        try:
            s.sendall(build_message())
        except socket.error, (value, message):
            print 'send error: ' + message
            break
        time.sleep(6)

while 1:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host,port))
    except socket.error, (value, message):
        print 'connect error: ' + message
        s.close()
        time.sleep(1)
        continue
    communicate(s)
    s.close()

