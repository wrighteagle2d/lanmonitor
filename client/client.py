#!/usr/bin/env python

import re
import os
import time
import socket
import commands

host = "192.168.26.160"
port = 50000
server_count = 0

team_name_map = {
            re.compile("WE20"): "WrightEagle",
            re.compile("WrightEagle"): "WrightEagle",
            re.compile("helios_"): "Helios",
            re.compile("nq"): "LsuAmoyNQ",
            re.compile("oxsy"): "Oxsy",
            re.compile("BS2kAgent"): "BrainStormers",
            re.compile("SputCoach"): "BrainStormers",
            re.compile("NemesisAgent"): "Nemesis",
            re.compile("sample_"): "Agent2D",
            re.compile("ESKILAS"): "Eskilas"
        }

def build_message():
    message = ""

    message += uptime()
    message += process_status()
    message += test_info()

    return message 

def uptime():
    return commands.getoutput("uptime").strip()

def process_status():
    global server_count

    server_name = "rcssserver"
    server_user = ""
    server_count = 0

    process_list = commands.getoutput("ps -e -o comm,user=").strip().split("\n")
    process_list.pop(0)

    team_count_map = {}
    cmd_count_map = {}
    matched_cmds = {}

    for process in process_list:
        info = process.split()
        (cmd, user) = (info[0], info[1])

        cmd_count_map[cmd] = 1 + cmd_count_map.get(cmd, 0)
        for pattern in team_name_map.keys():
            if pattern.match(cmd):
                matched_cmds[cmd] = 1
                team_name = team_name_map[pattern]
                team_count_map[team_name] = 1 + team_count_map.get(team_name, 0)
                break

        if not server_user and cmd == server_name:
            server_user = user

    if cmd_count_map.has_key(server_name):
        server_count = cmd_count_map[server_name]

    message = ""

    if server_count:
        message += "; #rcss: %d" % server_count
        if server_user:
            message += ", %s" % server_user

    if len(team_count_map) >= 1:
        message += "; ("
        for team in sorted(team_count_map.keys()):
            message += "%s x %d, " % (team, team_count_map[team])
        message = message.rstrip(", ") + ")"

    return message

def test_info():
    message = ""

    if server_count > 0:
        if os.path.exists("/tmp/autotest::temp"):
            message += "; autotest::temp"

        if os.path.exists("/tmp/result.html") and os.access("/tmp/result.html", os.R_OK):
            game_count = commands.getoutput("cat /tmp/result.html | grep \'>Game&nbsp;Count\' | sed \'s/&nbsp;/ /g\' | awk \'{print $5}\'")
            win_rate = commands.getoutput("cat /tmp/result.html | grep \'&nbsp;WinRate\' |  sed \'s/&nbsp;/ /g\' | awk \'{print $6}\'").strip(",")

            if len(game_count) > 0 and len(win_rate) > 0:
                message += "; #game: " + game_count + ", " +  win_rate + "%"

    return message

def communicate(s):
    while 1:
        try:
            s.sendall(build_message())
        except socket.error, (value, message):
            print "send error: " + message
            break
        time.sleep(30)

def run():
    while 1:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((host,port))
        except socket.error, (value, message):
            print "connect error: " + message
            s.close()
            time.sleep(1)
            continue
        communicate(s)
        s.close()

run()
