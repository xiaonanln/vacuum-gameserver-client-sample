# encoding: utf8

import asyncore
import socket
import sys


class GSClient(asyncore.dispatcher_with_send):

    BUFFER_SIZE = 4096

    def __init__(self, host, port):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))

    def handle_read(self):
        print 'readable'
        data = self.recv(GSClient.BUFFER_SIZE)
        print data