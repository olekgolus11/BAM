from PodSixNet.Channel import Channel
from time import time


class ClientHandler(Channel):

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        print(self, 'Client disconnected')

    def Network_message(self, data):
        print(self, "Network_message work!")

    def PlayerInfo(self, playerData):
        print("Send player info!")
        self.Send({"action": "playerInfo", "playerInfo": {"id": playerData["id"], "x": playerData["x"], "y": playerData["y"]}})

    def PlayersInfo(self, data):
        print("Send players info!")
        self.Send({"action": "playersInfo", "playersInfo": data})

    def Message(self, data):
        self.Send({"action": "message", "message": data})