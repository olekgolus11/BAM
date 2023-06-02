from __future__ import print_function
from sys import exit
import pygame
from PodSixNet.Connection import connection, ConnectionListener
from Map.MapClient import MapClient
from Player import Player


class Client(ConnectionListener):
    player = None
    screen = None
    clock = None
    map = None

    def __init__(self, host, port):
        self.setupWindow()
        self.Connect((host, port))
        self.playersArray = [Player(60, 60, 1, self.screen), Player(120, 60, 2, self.screen), Player(60, 120, 3, self.screen)]
        self.imagePathArray = {"1": "", "2": "", "3": ""}
        print("Client started")

    def Network_message(self, data):
        print("got:", data['message'])
        connection.Send(data)
        connection.Pump()

    def sendPlayerInfo(self):
        connection.Send({"action": "playerInfo", "playerInfo":
            {"id": self.player.playerId, "x": self.player.x, "y": self.player.y, "imagePath": self.player.getImagePath()}})

    def Network_playersInfo(self, data):
        playersInfo = data["playersInfo"]
        for playerInfoElement in playersInfo:
            for player in self.playersArray:
                if playerInfoElement["id"] == player.playerId:
                    player.x = playerInfoElement["x"]
                    player.y = playerInfoElement["y"]
                    self.imagePathArray[str(player.playerId)] = playerInfoElement["imagePath"]

    def Network_playerInfo(self, data):
        info = data["playerInfo"]
        self.player = Player(info["x"], info["y"], info["id"], self.screen)
        self.imagePathArray[str(self.player.playerId)] = info["imagePath"]
        print("My info: ", "id: ", self.player.playerId,
              "x: ", self.player.x, "y: ", self.player.y, "imagePath: ", self.imagePathArray[str(self.player.playerId)])

    def Network_board(self, data):
        self.map.updateBoard(data['board'])
        connection.Pump()

    def Network_connected(self, data):
        print("Connected to the server")

    def Network_error(self, data):
        print('error:', data['error'][1])
        connection.Close()

    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()

    def Network_bombFromServer(self, data):
        for player in self.playersArray:
            if player.playerId == self.player.playerId:
                player.bombsHandler.dictionaryToBomb(data["bomb"])

    def setupWindow(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.screen.fill('black')
        self.clock = pygame.time.Clock()
        self.map = MapClient(self.screen)
        pygame.display.set_caption("BAM!")

    def sendTestMessage(self):
        connection.Send('Connection test')

    def update(self):
        connection.Pump()
        self.Pump()
        self.clock.tick(60)

    def drawAllPlayers(self):
        for player in self.playersArray:
            player.draw(self.imagePathArray[str(player.playerId)])
        pygame.display.update()

    def updatePlayerMap(self):
        self.player.map.updateBoard(self.map.board)

    def drawBoard(self):
        self.map.draw()

    def sendBombToServer(self, bomb):
        connection.Send({"action": "newBombFromPlayer", "bomb": self.player.bombsHandler.bombToDictionary(bomb)})

    def handleBombPlantedThisRound(self):
        if self.player.bombsHandler.bombPlantedThisRound:
            self.sendBombToServer(self.player.bombsHandler.bombPlantedThisRound)
            self.player.bombsHandler.bombPlantedThisRound = 0

    def run(self):
        running = True
        while running:
            self.update()
            self.updatePlayerMap()
            self.player.run()
            self.drawAllPlayers()
            self.drawBoard()
            self.sendPlayerInfo()
            self.player.bombsHandler.updateBombTimers()
            self.handleBombPlantedThisRound()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()


client = Client("localhost", 3000)
#TODO: Change spinlock to something better
while client.player is None:
    client.update()
client.run()
