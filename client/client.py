#!/usr/bin/env python

import os
import re
import sys
import time
import socket

host = '192.168.26.160'
port = 50000

team_name_map = {
        re.compile('WE20\d\d'): 'WrightEagle',
        re.compile('helios'): 'Helios',
        re.compile('nq{player,coach}'): 'LsuAmoyNQ',
        re.compile('oxsy'): 'Oxsy',
        re.compile('BS2k'): 'BrainStormer'
        }

def get_output(cmd) :
    pipe = os.popen(cmd)
    output = pipe.read()
    pipe.close()
    return output

def build_message( ) :
    message = uptime() + ", "
    message += rcssserver()
    return message 

def uptime() :
    return get_output('uptime').strip()

def find_testing_teams() :
    teams = []
    process_list = get_output("ps -o comm= -e | sort | uniq").strip().split('\n')
    for process in process_list :
        for pattern in team_name_map.keys() :
            if pattern.match(process) :
                teams.append(team_name_map[pattern])
                break
        if len(teams) >= 2 :
            break
    return teams

def rcssserver() :
    output = get_output('ps -o user= -C rcssserver').split('\n');
    count = len(output) - 1;
    message = ' #rcssserver: '
    if count > 0:
        message += '%d,%s' % (count, output[0])
        teams = find_testing_teams()
        if len(teams) > 0 :
            message += ' ('
            for team in teams :
                message += team + ','
            message = message.strip(',') + ')'
    else :
        message += '0'
    return message

def communicate(s) :
    while 1:
        try:
            s.sendall(build_message())
        except socket.error, (value, message):
            print 'send error: ' + message
            break
        time.sleep(10)

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

