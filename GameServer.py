from __future__ import print_function

from time import sleep
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server

from ClientHandler import ClientHandler


class GameServer(Server):
    channelClass = ClientHandler

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        print('Server launched')

    def AddPlayer(self, player):
        self.players[player] = True
        print("New Player: " + str(player.addr))
        print("Connected players: ", [p for p in self.players])

    def DelPlayer(self, player):
        print("Deleting Player" + str(player.addr))
        del self.players[player]

    def SendToAll(self, data):
        [p.Message(data) for p in self.players]

    def SendPlayers(self):
        self.SendToAll({"action": "players", "players": [p.addr for p in self.players]})

    def Connected(self, channel, addr):
        print(channel, "Channel connected")
        self.AddPlayer(channel)
        self.SendToAll({"action": "message", "message": str(addr) + " connected"})

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)


# get command line argument of server, port
s = GameServer(localaddr=('localhost', 3000))
s.Launch()