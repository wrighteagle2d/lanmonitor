#!/usr/bin/env python

import os
import sys
import time
import select
import socket
import threading

g_client_table = { }
g_mutex = threading.Lock()

g_html_head = '''<head> 
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
<meta http-equiv="refresh" content="2">
<link type="text/css" rel="stylesheet" href="./style.css">
<title> WrightEagle 2D Lan Server Status</title> 
</head>

<body>
<h1>LAN Server Status</h1>
<hr>
'''

g_html_tail= '''
<hr>
</body>'''

class Server:
    def __init__(self):
        self.host = ''
        self.port = 50000
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):
        while 1 :
            try:
                self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server.bind((self.host,self.port))
                self.server.listen(5)
                break
            except socket.error, (value,message):
                if self.server:
                    self.server.close()
                print "Could not open socket: " + message
                time.sleep(1)


    def run(self):
        generate_html()

        self.open_socket()
        running = 1
        while running:
            c = Client(self.server.accept())
            c.start()
            self.threads.append(c)

        # close all threads

        self.server.close()
        for c in self.threads:
            c.join()

class Client(threading.Thread):
    def __init__(self,(client,address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024

    def run(self):
        running = 1
        while running:
            message = self.client.recv(self.size)

            g_mutex.acquire()
            if message:
                g_client_table[self.address[0]] = message
            else:
                del g_client_table[self.address[0]]
                self.client.close()
                running = 0
            generate_html()
            g_mutex.release()

def generate_html() :
    html_content = g_html_head
    for client in sorted(g_client_table.keys()) :
        html_content += '<p><strong>' + client + '</strong>: ' + g_client_table[client] + '</p>\n' 
    html_content += g_html_tail

    index_html = open('index.html', 'w')
    index_html.write(html_content)
    index_html.close()

Server().run()
