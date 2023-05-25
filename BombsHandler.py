from Bomb import Bomb
import pygame
from constants import *

class BombsHandler:

    def __init__(self):
        self.everyPlayersBombs = []
        self.bombPlantedThisRound = None
        self.isBombPlantedThisRound = False
        self.myBombsTimers = []
        self.maxBombsPlanted = 3
        self.myBombsPlanted = 0
        self.bombPower = 3

    def drawBombs(self, screen):
        for bomb in self.everyPlayersBombs:
            if bomb.timer >= FOURTH_BOMB_STATE:
                self.everyPlayersBombs.remove(bomb)
            else:
                bomb.draw(screen)

    def addBomb(self, x, y):
        if self.myBombsPlanted < self.maxBombsPlanted and self.isBombPlantedThisRound is False:
            self.myBombsTimers.append(0)
            self.bombPlantedThisRound = Bomb(x, y, self.bombPower)
            self.isBombPlantedThisRound = True
            self.myBombsPlanted += 1

    def dictionaryToBomb(self, dictBomb):
        x = dictBomb["x"]
        y = dictBomb["y"]
        power = dictBomb["power"]
        self.everyPlayersBombs.append(Bomb(x, y, power))

    def bombToDictionary(self, bomb):
        return {"x": bomb.x, "y": bomb.y, "power": bomb.power}

    def updateBombTimers(self):
        index = None
        toRemove = False
        for i in range(0, len(self.myBombsTimers)):
            if self.myBombsTimers[i] < FOURTH_BOMB_STATE:
                self.myBombsTimers[i] += 1
            else:
                index = i
                toRemove = True
        if toRemove:
            self.myBombsTimers.pop(index)
            self.myBombsPlanted -= 1