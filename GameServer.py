from __future__ import print_function
from time import sleep
from weakref import WeakKeyDictionary
from PodSixNet.Server import Server
from ClientHandler import ClientHandler
from PlayerInfo import PlayerInfo
from Map.MapServer import MapServer


class GameServer(Server):
    channelClass = ClientHandler
    idArray = [0, 0, 0]
    playersInfoArray = []

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        print('Server launched')
        self.map = MapServer

    def addPlayer(self, channel):
        playerinfo = PlayerInfo(0,0, self.getNewId(), channel)
        self.playersInfoArray.append({"id": playerinfo.id, "x": playerinfo.x, "y": playerinfo.y, "channel": playerinfo.channel})

    def getNewId(self):
        for i in range(0, 2):
            if self.idArray[i] == 0:
                self.idArray[i] = 1
                return i+1

    def delPlayer(self, channel):
        for i in range(0, len(self.playersInfoArray)):
            if self.playersInfoArray[i]["channel"] == channel:
                self.playersInfoArray.pop(i)

    def sendAllPlayersDataToAll(self):
        playersInfo = self.preparePlayerInfoArray()
        for i in range(0, len(self.playersInfoArray)):
            playerChannel = self.playersInfoArray[i]["channel"]
            playerChannel.PlayersInfo(playersInfo)

    def preparePlayerInfoArray(self):
        playersInfo = []
        for i in range(0, len(self.playersInfoArray)):
            player = self.playersInfoArray[i]
            playersInfo.append({"id": player["id"], "x": player["x"], "y": player["y"]})
        return playersInfo

    def sendInfoToPlayer(self, channel):
        for i in range(0, len(self.playersInfoArray)):
            if self.playersInfoArray[i]["channel"] == channel:
                channel.PlayerInfo(self.playersInfoArray[i])

    def Connected(self, channel, addr):
        print(channel, "Channel connected")
        self.addPlayer(channel)
        self.sendInfoToPlayer(channel)
        self.sendAllPlayersDataToAll()
        print(self.map.board)
        channel.Send({"action": "board", "board": self.map.board})

    def launch(self):
        while True:
            self.Pump()
            sleep(0.0001)


# get command line argument of server, port
s = GameServer(localaddr=('localhost', 3000))
s.launch()
