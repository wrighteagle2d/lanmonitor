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

def rcssserver() :
    return ' #rcssserver %d' % (len(get_output('ps -o pid= -C rcssserver').split('\n')) - 1)

def communicate(s) :
    while 1:
        try:
            s.sendall(build_message())
        except socket.error, (value, message):
            print 'send error: ' + message
            break
        time.sleep(5)

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

