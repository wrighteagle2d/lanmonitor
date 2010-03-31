#!/usr/bin/env python

import os
import re
import sys
import time
import random
import socket

host = '192.168.26.160'
port = 50000

team_name_map = {
            re.compile('WE20'): 'WrightEagle',
            re.compile('helios'): 'Helios',
            re.compile('nq'): 'LsuAmoyNQ',
            re.compile('oxsy'): 'Oxsy',
            re.compile('BS2kAgent'): 'BrainStormer',
            re.compile('SputCoach'): 'BrainStormer'
        }

def get_output(cmd) :
    pipe = os.popen(cmd)
    output = pipe.read()
    pipe.close()
    return output

def build_message() :
    message = uptime() + ", "
    message += rcssserver()
    return message 

def uptime() :
    return get_output('uptime').strip()

def find_testing_team_map() :
    team_map = {}
    process_map = {}
    matched_process_map = {}

    process_list = get_output("ps -o comm= -e").strip().split('\n')

    for process in process_list :
        process_map[process] = 1 + process_map.get(process, 0)
        for pattern in team_name_map.keys() :
            if pattern.match(process) :
                matched_process_map[process] = 1
                team_name = team_name_map[pattern]
                team_map[team_name] = 1 + team_map.get(team_name, 0)
                break

    if len(team_map) <= 1 :
        count_map = {}
        for process in process_map.keys() :
            count_map.setdefault(process_map[process], []).append(process)
        count_list = count_map.keys()
        count_list.sort()
        count_list.reverse()
        for count in count_list :
            for process in count_map[count] :
                if not matched_process_map.has_key(process) :
                    team_map['[' + process + ']'] = process_map[process]
                    if len(team_map) >= 2 :
                        return team_map

    return team_map

def rcssserver() :
    output = get_output('ps -o user= -C rcssserver').split('\n');
    count = len(output) - 1;
    message = ' #rcssserver: '
    if count > 0:
        message += '%d,%s' % (count, output[0])
        team_map = find_testing_team_map()
        if len(team_map) > 0 :
            message += ' ('
            for team in sorted(team_map.keys()) :
                message += '%s x %s, ' % (team, team_map[team])
            message = message.rstrip(', ') + ')'
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


def run() :
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

run()
