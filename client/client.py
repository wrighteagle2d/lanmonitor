#!/usr/bin/env python

import socket
import sys
import time
import subprocess

host = '192.168.26.160'
port = 50000

def build_message( ):
    message = uptime().strip() + ", "
    message += rcssserver()
    return message 

def uptime() :
    command = subprocess.Popen(['uptime'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return command.communicate()[0]

def rcssserver() :
    command = subprocess.Popen(['ps', '-o', 'pid=', '-C', 'rcssserver'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return ' #rcssserver %d' % (len(command.communicate()[0].split('\n')) - 1)

def sending(s) :
    while 1:
        try:
            s.sendall(build_message())
        except socket.error, (value, message):
            print 'send error: ' + message
            s.close()
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
    sending(s)
    s.close()

