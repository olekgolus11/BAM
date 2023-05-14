from __future__ import print_function

import sys
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener


class LagTimeClient(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))
        print("LagTimeClient started")

    def Network_ping(self, data):
        print("got:", data)
        if data["count"] == 10:
            connection.Close()
        else:
            connection.Send(data)

    # built in stuff

    def Network_connected(self, data):
        print("Connected to the server")

    def Network_error(self, data):
        print('error:', data['error'][1])
        connection.Close()

    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()


c = LagTimeClient("localhost", 3000)
while 1:
    connection.Pump()
    c.Pump()
    sleep(0.001)