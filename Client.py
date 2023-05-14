from __future__ import print_function

import sys
from time import sleep
from sys import stdin, exit

import pygame
from PodSixNet.Connection import connection, ConnectionListener
from Player import Player

class Client(ConnectionListener):
    player = None

    def __init__(self, host, port):
        self.Connect((host, port))
        self.player = Player(1,2)
        print("Client started")

    def Network_message(self, data):
        print("got:", data['message'])
        connection.Send(data)
        connection.Pump()
        # connection.Close()


    def Network_connected(self, data):
        print("Connected to the server")

    def Network_error(self, data):
        print('error:', data['error'][1])
        connection.Close()

    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()

    def setupWindow(self):
        pygame.init()
        screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Bomberman")
        screen.fill((0, 0, 0))
        pygame.display.update()



c = Client("192.168.18.35", 3000)

while 1:
    connection.Pump()
    c.Pump()
    connection.Send('Connection test')
    sleep(1)