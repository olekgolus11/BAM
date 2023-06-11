from __future__ import print_function

import sys

import pygame
from PodSixNet.Connection import connection, ConnectionListener
from Map.MapClient import MapClient
from Player import Player
from Menu.Menu import Menu
from constants import *
from utilities import MenuState, getTileCoordinates


class Client(ConnectionListener):
    player = None
    screen = None
    clock = None
    map = None
    menu = None
    score = None
    isRoundOver = None
    isRoundWon = None
    playersPointsArray = None
    runningMenu = None
    menuState = None
    seed = None

    def __init__(self, host, port):
        self.setupWindow()
        self.runningMenu = True
        self.menuState = MenuState.MENU
        self.menu = Menu()
        self.score = 0
        self.host = host
        self.port = port
        self.playersArray = [Player(PLAYER_1_X_POS, PLAYER_1_Y_POS, 1, self.screen),
                             Player(PLAYER_2_X_POS, PLAYER_2_Y_POS, 2, self.screen),
                             Player(PLAYER_3_X_POS, PLAYER_3_Y_POS, 3, self.screen)]
        self.playersPointsArray = [0, 0, 0]
        self.shouldLoadSong = True
        self.imagePathArray = {"1": "", "2": "", "3": ""}
        self.isRoundOver = False
        print("Client started")

    def connectClient(self):
        self.Connect((self.host, self.port))

    def Network_message(self, data):
        print("got:", data['message'])
        connection.Send(data)
        connection.Pump()

    def sendPlayerInfo(self):
        connection.Send({"action": "playerInfo", "playerInfo":
            {"id": self.player.playerId, "x": self.player.x, "y": self.player.y,
             "imagePath": self.player.getImagePath()}})

    def Network_playersInfo(self, data):
        playersInfo = data["playersInfo"]
        for playerInfoElement in playersInfo:
            for player in self.playersArray:
                if playerInfoElement["id"] == player.playerId:
                    if player.playerId != self.player.playerId:
                        player.x = playerInfoElement["x"]
                        player.y = playerInfoElement["y"]
                    self.imagePathArray[str(player.playerId)] = playerInfoElement["imagePath"]

    def Network_resetPlayersInfo(self, data):
        self.isRoundOver = False
        self.isRoundWon = None
        playersInfo = data["playersInfo"]
        for playerInfoElement in playersInfo:
            for player in self.playersArray:
                if playerInfoElement["id"] == player.playerId:
                    player.x = playerInfoElement["x"]
                    player.y = playerInfoElement["y"]
                    player.alive = playerInfoElement["alive"]
                    self.imagePathArray[str(player.playerId)] = playerInfoElement["imagePath"]

    def Network_playerInfo(self, data):
        info = data["playerInfo"]
        self.player = self.playersArray[info["id"] - 1]
        self.imagePathArray[str(self.player.playerId)] = info["imagePath"]
        print("My info: ", "id: ", self.player.playerId,
              "x: ", self.player.x, "y: ", self.player.y, "imagePath: ", self.imagePathArray[str(self.player.playerId)])

    def Network_board(self, data):
        self.map.updateBoard(data['board'])
        connection.Pump()

    def Network_seed(self, data):
        self.player.bombsHandler.map.updateSeed(data["seed"])
        connection.Pump()

    def Network_connected(self, data):
        print("Connected to the server")

    def Network_error(self, data):
        print('error:', data['error'][1])
        connection.Close()

    def Network_disconnected(self, data):
        print('Server disconnected')
        sys.exit()

    def Network_bombFromServer(self, data):
        connection.Pump()
        for player in self.playersArray:
            if player.playerId == self.player.playerId:
                player.bombsHandler.dictionaryToBomb(data["bomb"])

    def Network_pointToWinner(self, data):
        self.score += 1
        connection.Pump()
        self.Pump()

    def Network_playersPoints(self, data):
        self.playersPointsArray = data["score"]

    def Network_roundOver(self, data):
        self.player.resetPlayerPowers()
        connection.Pump()
        self.Pump()
        self.isRoundOver = True
        if self.player.playerId == data["winnerId"]:
            self.isRoundWon = True
        self.updatePlayerMap()

    def Network_resetGame(self, data):
        self.isRoundOver = False
        self.isRoundWon = None
        self.score = 0
        self.runningMenu = True
        self.player.bombsHandler.bombs = []
        self.player.bombsHandler.myBombs = []
        connection.Pump()
        self.Pump()
        self.updatePlayerMap()

    def PlayerDead(self):
        connection.Send({"action": "playerDead", "playerId": self.player.playerId})

    def drawRoundScoreMessage(self):
        if not self.isRoundOver:
            return
        if self.isRoundWon is True:
            self.player.drawYouWon(self.score)
        self.player.drawScore(self.score)

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

    def handlePowerUp(self):
        for player in self.playersArray:
            y, x = getTileCoordinates(player.y, player.x)
            if self.player.map.board[y][x] == MORE_BOMBS:
                player.bombsHandler.maxBombsPlanted += 1
            elif self.player.map.board[y][x] == MORE_POWER:
                player.bombsHandler.bombRange += 1
            elif self.player.map.board[y][x] == MORE_SPEED:
                if player.speed < 6:
                    self.handlePlayerSpeedUP(player)
            self.player.map.board[y][x] = FLOOR

    def handlePlayerSpeedUP(self, player):
        player.speed += 1
        y = player.y // player.speed
        x = player.x // player.speed
        player.x = x * player.speed
        player.y = y * player.speed

    def sendBombToServer(self, bomb):
        connection.Send({"action": "newBombFromPlayer", "bomb": self.player.bombsHandler.bombToDictionary(bomb)})
        connection.Pump()

    def handleBombPlantedThisRound(self):
        if self.player.bombsHandler.bombPlantedThisRound:
            self.sendBombToServer(self.player.bombsHandler.bombPlantedThisRound)
            self.player.bombsHandler.bombPlantedThisRound = None

    def updatePlayerMap(self):
        self.Pump()
        self.player.map.updateBoard(self.map.board)

    def handleBombs(self):
        for player in self.playersArray:
            if player.playerId == self.player.playerId:
                player.bombsHandler.updateBombs()
        self.player.bombsHandler.updateMyBombs()
        self.handleBombPlantedThisRound()

    def handlePlayerHit(self):
        if self.player.isPlayerHit() is True and self.player.alive is True:
            self.player.alive = False
            self.PlayerDead()

    def drawPlayersInLobby(self):
        for i in range(0, len(self.imagePathArray)):
            if self.imagePathArray[str(i + 1)] != "":
                self.menu.drawPlayerInLobby(i + 1)
                pygame.display.update()

    def allPlayersJoined(self):
        if self.imagePathArray["1"] != "" and self.imagePathArray["2"] != "" and self.imagePathArray["3"] != "":
            return True
        return False

    def startSong(self):
        pygame.mixer.music.load("assets/sounds/menu_music.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def startInGameSong(self):
        if self.shouldLoadSong is True:
            pygame.mixer.music.load("assets/sounds/ingame_music.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
            self.shouldLoadSong = False

    def startCountdown(self):
        pygame.mixer.music.load("assets/sounds/countdown.mp3")
        pygame.mixer.music.play()
        self.shouldLoadSong = True

    def runGame(self):
        self.update()
        self.handlePlayerHit()
        self.drawRoundScoreMessage()
        self.handlePowerUp()
        if self.player.alive is True:
            self.player.run()
        else:
            self.player.drawYouDied()
        self.drawAllPlayers()
        self.drawBoard()
        self.sendPlayerInfo()
        self.handleBombs()
        self.menu.showStats(self.playersPointsArray)

    def runMenu(self):
        menuState = MenuState.MENU
        self.update()
        self.sendPlayerInfo()
        if self.menuState == MenuState.LOBBY:
            if self.menu.showLobby() == MenuState.MENU:
                self.menuState = MenuState.MENU
            else:
                self.drawPlayersInLobby()
        elif self.menu.showMenu() == MenuState.LOBBY:
            self.menuState = MenuState.LOBBY
        if self.allPlayersJoined():
            self.startCountdown()
            self.menu.showCountDownTimer()
            self.runningMenu = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def run(self):
        self.runningMenu = True
        running = True
        self.startSong()
        while running:
            if self.runningMenu:
                self.runMenu()
            else:
                self.startInGameSong()
                self.runGame()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()


client = Client("", PORT)
client.host = client.menu.showJoinScreen()
print(client.host)
client.connectClient()
# TODO: Change spinlock to something better
client.setupWindow()
while client.player is None:
    client.update()
client.run()
