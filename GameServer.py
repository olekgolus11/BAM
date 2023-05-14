from __future__ import print_function

from time import sleep, localtime
from weakref import WeakKeyDictionary
from time import time
import sys

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel


class LagTimeChannel(Channel):

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.count = 0
        self.times = []

    def Close(self):
        print(self, 'Client disconnected')

    def Network_ping(self, data):
        print(self, "ping %d round trip time was %f" % (data["count"], time() - self.times[data["count"]]))
        self.Ping()

    def Ping(self):
        print(self, "Ping:", self.count)
        self.times.append(time())
        self.Send({"action": "ping", "count": self.count})
        self.count += 1


class LagTimeServer(Server):
    channelClass = LagTimeChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        print('Server launched')

    def Connected(self, channel, addr):
        print(channel, "Channel connected")
        channel.Ping()

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)


# get command line argument of server, port
s = LagTimeServer(localaddr=('localhost', 3000))
s.Launch()