from __future__ import print_function

import sys
from time import sleep
from sys import stdin, exit

import pygame
from PodSixNet.Connection import connection, ConnectionListener
from Player import Player


class Client(ConnectionListener):
    player = None
    screen = None
    clock = None

    def __init__(self, host, port):
        self.Connect((host, port))
        self.player = Player(1, 2)
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
        self.screen = pygame.display.set_mode((1280, 720))
        self.screen.fill('black')
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("BAM!")

    def sendTestMessage(self):
        connection.Send('Connection test')

    def update(self):
        connection.Pump()
        self.Pump()
        self.sendTestMessage()
        self.clock.tick(60)

    def drawPlayer(self):
        self.player.draw(self.screen)
        pygame.display.update()
        self.screen.fill('black')

    def run(self):
        running = True
        while running:
            self.update()
            self.player.move()
            self.drawPlayer()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()


client = Client("192.168.18.35", 3000)
client.setupWindow()
client.run()

