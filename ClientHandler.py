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

    def RoundOver(self):
        self.Send({"action": "roundOver", "winnerId": self._server.getWinner()})
        self.Pump()

    def ResetGame(self):
        self.Send({"action": "resetGame", "resetGame": True})
        self.Pump()

    def Message(self, data):
        self.Send({"action": "message", "message": data})

    def Network_newBombFromPlayer(self, data):
        for i in range(0, len(self._server.playersInfoArray)):
            playerChannel = self._server.playersInfoArray[i]["channel"]
            playerChannel.Send({"action": "bombFromServer", "bomb": data["bomb"]})

    def Board(self, data):
        self.Send({"action": "board", "board": data})
        self.Pump()

    def Seed(self, seed):
        self.Send({"action": "seed", "seed": seed})

    def PointToWinner(self):
        self.Send({"action": "pointToWinner", "winner": True})
        self.Pump()

    def Network_playerDead(self, data):
        self._server.playersInfoArray[data["playerId"] - 1]["alive"] = False
        if self._server.isRoundOver():
            # TODO: Handle adding points to player
            self._server.sendRoundOverToAllPlayers()
            self._server.addPointToWinner()
            self._server.resetRound()
        if self._server.isGameOver():
            self._server.resetGame()

