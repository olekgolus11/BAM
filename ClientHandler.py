from PodSixNet.Channel import Channel
from time import time


class ClientHandler(Channel):

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        print(self, 'Client disconnected')

    def Network_message(self, data):
        print(self, data)

    def Message(self, data):
        print(self, "Sending message")
        self.Send({"action": "message", "message": data})