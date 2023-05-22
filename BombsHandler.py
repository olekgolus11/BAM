from Bomb import Bomb
import pygame
from Constants import *

class BombsHandler:

    def __init__(self):
        self.everyPlayersBombs = []
        self.bombPlantedThisRound = 0
        self.myBombsTimers = []
        self.maxBombsPlanted = 3
        self.myBombsPlanted = 0
        self.bombPower = 3
        self.bombPlacedThisRound = False

    def printBombs(self, screen):
        for bomb in self.everyPlayersBombs:
            if bomb.timer >= FOURTH_BOMB_STATE:
                bomb.__del__()
                self.everyPlayersBombs.remove(bomb)
            else:
                bomb.plant(screen)

    def addBomb(self, key, x, y):
        if key[pygame.K_SPACE]:
            if self.myBombsPlanted < self.maxBombsPlanted and self.bombPlacedThisRound == False:
                self.myBombsTimers.append(0)
                self.bombPlantedThisRound = Bomb(x, y, self.bombPower)
                self.bombPlacedThisRound = True
                self.myBombsPlanted += 1
        else:
            self.bombPlacedThisRound = False

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
            print(i)
            if self.myBombsTimers[i] < FOURTH_BOMB_STATE:
                self.myBombsTimers[i] += 1
            else:
                index = i
                toRemove = True
        if toRemove:
            self.myBombsTimers.pop(index)
            self.myBombsPlanted -= 1