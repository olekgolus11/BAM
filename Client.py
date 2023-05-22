from __future__ import print_function

import sys
from time import sleep
from sys import stdin, exit

import pygame
from PodSixNet.Connection import connection, ConnectionListener
from Player import Player
from PlayerInfo import PlayerInfo

class Client(ConnectionListener):
    player = None
    screen = None
    clock = None

    def __init__(self, host, port):
        self.Connect((host, port))
        print("Client started")

    def Network_message(self, data):
        print("got:", data['message'])
        connection.Send(data)
        connection.Pump()

    def Network_playersInfo(self, data):
        playersInfo = data["playersInfo"]
        print("Players info: ", playersInfo)

    def Network_playerInfo(self, data):
        info = data["playerInfo"]
        self.player = Player(info["x"], info["y"], info["id"])
        print("My info: ", "id: ", self.player.playerId, "x: ", self.player.x, "y: ", self.player.y)

    def Network_connected(self, data):
        print("Connected to the server")

    def Network_error(self, data):
        print('error:', data['error'][1])
        connection.Close()

    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()

    def Network_bombFromServer(self, data):
        self.player.bombsHandler.dictionaryToBomb(data["bomb"])

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
        # self.sendTestMessage()
        self.clock.tick(60)

    def drawPlayer(self):
        self.player.draw(self.screen)
        pygame.display.update()
        self.screen.fill('black')

    def sendBombToServer(self, bomb):
        connection.Send({"action": "newBombFromPlayer", "bomb": self.player.bombsHandler.bombToDictionary(bomb)})

    def run(self):
        running = True
        while running:
            self.update()
            self.player.move()
            self.drawPlayer()
            self.player.bombsHandler.updateBombTimers()
            if self.player.bombsHandler.bombPlantedThisRound:
                self.sendBombToServer(self.player.bombsHandler.bombPlantedThisRound)
                self.player.bombsHandler.bombPlantedThisRound = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()


client = Client("localhost", 3000)
client.setupWindow()
client.run()
