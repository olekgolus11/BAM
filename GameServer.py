from __future__ import print_function

import sys
from time import sleep
from weakref import WeakKeyDictionary
from PodSixNet.Server import Server
from ClientHandler import ClientHandler
from PlayerInfo import PlayerInfo
from Map.MapServer import MapServer
from constants import *
from utilities import generateSeed


class GameServer(Server):
    channelClass = ClientHandler
    idArray = []
    playersInfoArray = []
    playersPointsArray = []
    playersConnected = None

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        print('Server launched')
        self.map = MapServer()
        self.idArray = [0, 0, 0]
        self.playersPointsArray = [0, 0, 0]
        self.seed = generateSeed()
        self.playersConnected = 0

    def addPlayer(self, channel):
        self.playersConnected += 1
        playerInfo = PlayerInfo(TILE_SIZE, TILE_SIZE, self.getNewId(), channel, "")
        playerInfo.imagePath = self.getPlayerImagePath(playerInfo.id)
        self.playersInfoArray.append(
            {"id": playerInfo.id,
             "x": playerInfo.x,
             "y": playerInfo.y,
             "channel": playerInfo.channel,
             "imagePath": playerInfo.imagePath,
             "alive": playerInfo.alive})

    def getPlayerImagePath(self, PlayerId):
        return f"assets/player/char{PlayerId}_front_standing.png"

    def getNewId(self):
        for i in range(0, len(self.idArray)):
            if self.idArray[i] == 0:
                self.idArray[i] = 1
                return i + 1

    def sendKilledPlayer(self, playerId):
        for i in range(0, len(self.playersInfoArray)):
            if i + 1 == playerId:
                continue
            self.playersInfoArray[i]["channel"].KillPlayer(playerId)

    def delPlayer(self, channel):
        for i in range(0, len(self.playersInfoArray)):
            if self.playersInfoArray[i]["channel"] == channel:
                self.playersInfoArray.pop(i)

    def sendAllPlayersDataToAll(self):
        playersInfo = self.preparePlayerInfoArray()
        for i in range(0, len(self.playersInfoArray)):
            playerChannel = self.playersInfoArray[i]["channel"]
            playerChannel.PlayersInfo(playersInfo)

    def sendAllResetPlayersDataToAll(self):
        playersInfo = self.preparePlayerInfoArray()
        for i in range(0, len(self.playersInfoArray)):
            playerChannel = self.playersInfoArray[i]["channel"]
            playerChannel.ResetPlayersInfo(playersInfo)

    def preparePlayerInfoArray(self):
        playersInfo = []
        for i in range(0, len(self.playersInfoArray)):
            player = self.playersInfoArray[i]
            playersInfo.append(
                {"id": player["id"],
                 "x": player["x"],
                 "y": player["y"],
                 "imagePath": player["imagePath"],
                 "alive": player["alive"]})
        return playersInfo

    def getWinner(self):
        for i in range(0, len(self.playersInfoArray)):
            if self.playersInfoArray[i]["alive"] is True:
                return self.playersInfoArray[i]["id"]

    def sendInfoToPlayer(self, channel):
        for i in range(0, len(self.playersInfoArray)):
            if self.playersInfoArray[i]["channel"] == channel:
                channel.PlayerInfo(self.playersInfoArray[i])

    def addPointToWinner(self):
        self.playersPointsArray[self.getWinner() - 1] += 1
        self.sendPointToWinner()

    def sendPlayersPoints(self):
        for i in range(0, len(self.playersInfoArray)):
            playerChannel = self.playersInfoArray[i]["channel"]
            playerChannel.PlayersPoints()

    def sendPointToWinner(self):
        playerChannel = self.playersInfoArray[self.getWinner() - 1]["channel"]
        playerChannel.PointToWinner()

    def sendRoundOverToAllPlayers(self):
        for i in range(0, len(self.playersInfoArray)):
            playerChannel = self.playersInfoArray[i]["channel"]
            playerChannel.RoundOver()

    def sendResetGameToAllPlayers(self):
        self.seed = generateSeed()
        for i in range(0, len(self.playersInfoArray)):
            playerChannel = self.playersInfoArray[i]["channel"]
            playerChannel.ResetGame()
            self.sendSeed(playerChannel)

    def sendBoardToPlayer(self, channel):
        channel.Board(self.map.board)

    def sendSeed(self, channel):
        channel.Seed(self.seed)

    def isRoundOver(self):
        alivePlayers = 0
        for i in range(0, len(self.playersInfoArray)):
            if self.playersInfoArray[i]["alive"] is True:
                alivePlayers += 1
        return alivePlayers <= 1

    def isGameOver(self):
        for i in range(0, len(self.playersPointsArray)):
            if self.playersPointsArray[i] == ROUNDS_TO_WIN_GAME:
                return True
        return False

    def resetGame(self):
        self.playersPointsArray = [0, 0, 0]
        self.sendResetGameToAllPlayers()

    def Connected(self, channel, addr):
        print(channel, "Channel connected")
        self.addPlayer(channel)
        self.sendInfoToPlayer(channel)
        self.sendBoardToPlayer(channel)
        self.sendSeed(channel)

    def isOnePlayerLeft(self):
        return self.playersConnected == 1

    def disconnectAllPlayers(self):
        for i in range(0, len(self.playersInfoArray)):
            playerChannel = self.playersInfoArray[i]["channel"]
            playerChannel.Disconnect()
            playerChannel.Pump()

    def launch(self):
        while True:
            if len(self.playersInfoArray) == 3 and self.isOnePlayerLeft():
                self.disconnectAllPlayers()
                sys.exit()
            self.sendAllPlayersDataToAll()
            self.Pump()
            sleep(0.0001)

    def getPlayerStartingPosition(self, playerId):
        if playerId == 1:
            return [PLAYER_1_X_POS, PLAYER_1_Y_POS]
        elif playerId == 2:
            return [PLAYER_2_X_POS, PLAYER_2_Y_POS]
        elif playerId == 3:
            return [PLAYER_3_X_POS, PLAYER_3_Y_POS]

    def resetRound(self):
        sleep(RESET_ROUND_TIME)
        self.map = MapServer()
        for i in range(0, len(self.playersInfoArray)):
            self.playersInfoArray[i]["x"], self.playersInfoArray[i]["y"] = self.getPlayerStartingPosition(i + 1)
            self.playersInfoArray[i]["alive"] = True
        for i in range(0, len(self.playersInfoArray)):
            self.playersInfoArray[i]["channel"].Board(self.map.board)
        self.sendAllResetPlayersDataToAll()


# get command line argument of server, port
address = input("Input server address, or leave empty to run locally: ")
if not address:
    address = 'localhost'
print(f"Starting server on {address}:{PORT}")
s = GameServer(localaddr=(address, PORT))
s.launch()
