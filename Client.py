from __future__ import print_function
from sys import exit
import pygame
from PodSixNet.Connection import connection, ConnectionListener
from Map.MapClient import MapClient
from Player import Player
from Menu.Menu import Menu
from utilities import MenuState


class Client(ConnectionListener):
    player = None
    screen = None
    clock = None
    map = None
    menu = None

    def __init__(self, host, port):
        self.menu = Menu()
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

    def drawBoard(self):
        self.player.map.draw()

    def sendBombToServer(self, bomb):
        connection.Send({"action": "newBombFromPlayer", "bomb": self.player.bombsHandler.bombToDictionary(bomb)})

    def handleBombPlantedThisRound(self):
        if self.player.bombsHandler.bombPlantedThisRound:
            self.sendBombToServer(self.player.bombsHandler.bombPlantedThisRound)
            self.player.bombsHandler.bombPlantedThisRound = None

    def updatePlayerMap(self):
        self.player.map.updateBoard(self.map.board)

    def sendBoardToServer(self):
        connection.Send({"action": "boardToServer", "board": self.player.map.board})

    def handleBombs(self):
        for player in self.playersArray:
            if player.playerId == self.player.playerId:
                player.bombsHandler.updateBombs()
        self.player.bombsHandler.updateMyBombs()
        self.handleBombPlantedThisRound()

    def handlePlayerHit(self):
        if self.playersArray[self.player.playerId - 1].isPlayerHit() is True:
            self.player.alive = False

    def drawPlayersInLobby(self):
        for i in range(0, len(self.imagePathArray)):
            if self.imagePathArray[str(i+1)] != "":
                self.menu.drawPlayerInLobby(i+1)
                pygame.display.update()

    def allPlayersJoined(self):
        if self.imagePathArray["1"] != "" and self.imagePathArray["2"] != "" and self.imagePathArray["3"] != "":
            return True
        return False

    def run(self):
        menuState = MenuState.MENU
        running_menu = True
        while running_menu:
            self.update()
            self.sendPlayerInfo()
            if menuState == MenuState.LOBBY:
                self.menu.showLobby()
                self.drawPlayersInLobby()
            elif self.menu.showMenu() == MenuState.LOBBY:
                menuState = MenuState.LOBBY
            if self.allPlayersJoined():
                self.menu.showCountDownTimer()
                running_menu = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

        self.setupWindow()
        running = True
        while running:
            self.update()
            # self.updatePlayerMap()
            self.handlePlayerHit()
            if self.player.alive is True:
                self.player.run()
            self.drawAllPlayers()
            self.drawBoard()
            self.sendPlayerInfo()
            self.sendBoardToServer()
            self.handleBombs()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()


client = Client("localhost", 3000)
#TODO: Change spinlock to something better
client.setupWindow()
while client.player is None:
    client.update()
client.run()
