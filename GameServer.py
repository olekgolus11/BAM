from __future__ import print_function
from time import sleep
from weakref import WeakKeyDictionary
from PodSixNet.Server import Server
from ClientHandler import ClientHandler
from PlayerInfo import PlayerInfo
from Map.MapServer import MapServer
from constants import TILE_SIZE


class GameServer(Server):
    channelClass = ClientHandler
    idArray = [0, 0, 0]
    playersInfoArray = []
    playersPointsArray = []

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        print('Server launched')
        self.map = MapServer()
        self.playersPointsArray = [0, 0, 0]

    def addPlayer(self, channel):
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

    def sendPointToWinner(self):
        playerChannel = self.playersInfoArray[self.getWinner() - 1]["channel"]
        playerChannel.PointToWinner()

    def sendBoardToPlayer(self, channel):
        channel.Board(self.map.board)

    def isRoundOver(self):
        alivePlayers = 0
        for i in range(0, len(self.playersInfoArray)):
            if self.playersInfoArray[i]["alive"] is True:
                alivePlayers += 1
        return alivePlayers <= 1

    def Connected(self, channel, addr):
        print(channel, "Channel connected")
        self.addPlayer(channel)
        self.sendInfoToPlayer(channel)
        self.sendBoardToPlayer(channel)
        channel.Send({"action": "board", "board": self.map.board})

    def launch(self):
        while True:
            self.sendAllPlayersDataToAll()
            self.Pump()
            sleep(0.0001)

    def resetRound(self):
        sleep(2)
        print("Resetting round")
        # self.map = MapServer()
        for i in range(0, len(self.playersInfoArray)):
            self.playersInfoArray[i]["x"] = TILE_SIZE
            self.playersInfoArray[i]["y"] = TILE_SIZE
            self.playersInfoArray[i]["alive"] = True
        for i in range(0, len(self.playersInfoArray)):
            self.playersInfoArray[i]["channel"].Board(self.map.board)
        self.sendAllResetPlayersDataToAll()


# get command line argument of server, port
s = GameServer(localaddr=('localhost', 3000))
s.launch()
