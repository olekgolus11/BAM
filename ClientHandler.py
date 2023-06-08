from PodSixNet.Channel import Channel


class ClientHandler(Channel):

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        print(self, 'Client disconnected')

    def Network_message(self, data):
        print(self, "Network_message work!")

    def Network_playerInfo(self, data):
        playerInfo = data["playerInfo"]
        for player in self._server.playersInfoArray:
            if player["id"] == playerInfo["id"]:
                player["x"] = playerInfo["x"]
                player["y"] = playerInfo["y"]
                player["imagePath"] = playerInfo["imagePath"]
                break

    def PlayerInfo(self, playerData):
        self.Send({"action": "playerInfo", "playerInfo":
            {"id": playerData["id"], "x": playerData["x"], "y": playerData["y"], "imagePath": playerData["imagePath"]}})

    def PlayersInfo(self, data):
        self.Send({"action": "playersInfo", "playersInfo": data})

    def ResetPlayersInfo(self, data):
        self.Send({"action": "resetPlayersInfo", "playersInfo": data})

    def Message(self, data):
        self.Send({"action": "message", "message": data})

    def Network_newBombFromPlayer(self, data):
        for i in range(0, len(self._server.playersInfoArray)):
            playerChannel = self._server.playersInfoArray[i]["channel"]
            playerChannel.Send({"action": "bombFromServer", "bomb": data["bomb"]})

    def Network_boardToServer(self, data):
        for i in range(0, len(self._server.playersInfoArray)):
            playerChannel = self._server.playersInfoArray[i]["channel"]
            playerChannel.Board(data["board"])

    def Board(self, data):
        self.Send({"action": "board", "board": data})

    def PointToWinner(self):
        self.Send({"action": "pointToWinner", "winner": True})

    def Network_playerDead(self, data):
        print(self._server.playersPointsArray)
        self._server.playersInfoArray[data["playerId"] - 1]["alive"] = False
        if self._server.isRoundOver():
            # TODO: Handle adding points to player
            self._server.addPointToWinner()
            self._server.resetRound()
        print(self._server.playersPointsArray)

