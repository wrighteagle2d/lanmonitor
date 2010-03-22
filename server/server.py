#!/usr/bin/env python

import select
import socket
import sys
import threading
import os

class Server:
    def __init__(self):
        self.host = ''
        self.port = 50000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    def run(self):
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
            if message:
                f = open(self.address[0], 'w')
                message = '<p><strong>' + self.address[0] + '</strong>: \"' + message + '\"</p>\n' 
                f.write(message)
                f.close()
            else:
                self.client.close()
                running = 0

s = Server()
s.run()
