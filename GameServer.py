from __future__ import print_function

from time import sleep

from PodSixNet.Server import Server

from ClientHandler import ClientHandler


class GameServer(Server):
    channelClass = ClientHandler

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        print('Server launched')

    def Connected(self, channel, addr):
        print(channel, "Channel connected")
        channel.Message()

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)


# get command line argument of server, port
s = GameServer(localaddr=('localhost', 3000))
s.Launch()