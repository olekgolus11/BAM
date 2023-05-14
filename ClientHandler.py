from PodSixNet.Channel import Channel


class ClientHandler(Channel):

    def __init__(self, *args, **kwargs):
        print("new client")
        self.nickname = "anonymous"
        Channel.__init__(self, *args, **kwargs)

    def Network(self, data):
        print('hello')

    def Network_myaction(self, data):
        print("myaction:", data)

