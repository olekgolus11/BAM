from Bomb import Bomb
import pygame
import math

from Map.MapClient import MapClient
from constants import *
from utilities import getTileCoordinates


class BombsHandler:
    playerTileX = None
    playerTileY = None
    seed = None
    def __init__(self, mapFromPlayer: MapClient):
        self.map = mapFromPlayer
        self.everyPlayersBombs = []
        self.myBombs = []
        self.bombPlantedThisRound = None
        self.isBombPlantedThisRound = False
        self.maxBombsPlanted = 3
        self.myBombsPlanted = 0
        self.bombRange = 3

    def updateSeed(self, seed):
        self.seed = seed

    def updatePlayerTilePosition(self, x, y):
        self.playerTileY, self.playerTileX = getTileCoordinates(y, x)

    def drawBombs(self, screen):
        for bomb in self.everyPlayersBombs:
            bomb.draw(screen, self.map)

    def addBomb(self, x, y):
        if self.myBombsPlanted < self.maxBombsPlanted and self.isBombPlantedThisRound is False:
            self.bombPlantedThisRound = Bomb(x, y, self.bombRange)
            self.myBombs.append(Bomb(x, y, self.bombRange))
            self.isBombPlantedThisRound = True
            self.myBombsPlanted += 1

    def dictionaryToBomb(self, dictBomb):
        x = dictBomb["x"]
        y = dictBomb["y"]
        range = dictBomb["power"]
        self.everyPlayersBombs.append(Bomb(x, y, range))

    def bombToDictionary(self, bomb):
        return {"x": bomb.x, "y": bomb.y, "power": bomb.range}

    def isPlayerWithinExplosionRange(self, bomb):
        bombTileY, bombTileX = getTileCoordinates(bomb.y, bomb.x)
        distanceFromExplosionX = math.fabs(bombTileX - self.playerTileX)
        distanceFromExplosionY = math.fabs(bombTileY - self.playerTileY)
        if distanceFromExplosionX < bomb.range and distanceFromExplosionY < bomb.range:
            return True
        else:
            return False

    def isAnotherBombWithinExplosionRange(self, bomb, anotherBomb):
        bombTileY, bombTileX = getTileCoordinates(bomb.y, bomb.x)
        anotherBombTileY, anotherBombTileX = getTileCoordinates(anotherBomb.y, anotherBomb.x)
        distanceFromExplosionX = math.fabs(bombTileX - anotherBombTileX)
        distanceFromExplosionY = math.fabs(bombTileY - anotherBombTileY)
        if distanceFromExplosionX < bomb.range and distanceFromExplosionY < bomb.range:
            return True
        else:
            return False

    def isBehindTheWall(self, bomb, anotherBomb=None):
        bombTileY, bombTileX = getTileCoordinates(bomb.y, bomb.x)
        if anotherBomb is not None:
            otherObjectTileY, otherObjectTileX = getTileCoordinates(anotherBomb.y, anotherBomb.x)
        else:
            otherObjectTileY, otherObjectTileX = self.playerTileY, self.playerTileX

        isBehindTheWall = False

        if bombTileX == otherObjectTileX:
            for i in range(bombTileY, otherObjectTileY):
                if self.map.isTileAWall(i, otherObjectTileX):
                    isBehindTheWall = True
                    break
            for i in range(otherObjectTileY, bombTileY):
                if self.map.isTileAWall(i, otherObjectTileX):
                    isBehindTheWall = True
                    break
        elif bombTileY == otherObjectTileY:
            for i in range(bombTileX, otherObjectTileX):
                if self.map.isTileAWall(otherObjectTileY, i):
                    isBehindTheWall = True
                    break
            for i in range(otherObjectTileX, bombTileX):
                if self.map.isTileAWall(otherObjectTileY, i):
                    isBehindTheWall = True
                    break
        else:
            isBehindTheWall = True
        return isBehindTheWall

    def isPlayerBehindTheWall(self, bomb):
        return self.isBehindTheWall(bomb)

    def isAnotherBombBehindTheWall(self, bomb, anotherBomb):
        return self.isBehindTheWall(bomb, anotherBomb)

    def didBombExplodeOnPlayer(self):
        shouldPlayerDie = False
        for bomb in self.everyPlayersBombs:
            if shouldPlayerDie is True:
                return True
            if bomb.isExploded is True:
                if self.isPlayerWithinExplosionRange(bomb):
                    if self.isPlayerBehindTheWall(bomb):
                        shouldPlayerDie = False
                    else:
                        shouldPlayerDie = True
        return shouldPlayerDie

    def didBombHitAnotherBomb(self, anotherBomb):
        shouldAnotherBombExplode = False
        for bomb in self.everyPlayersBombs:
            if bomb is anotherBomb:
                continue
            if shouldAnotherBombExplode is True:
                return True
            if bomb.isExploded is True:
                if self.isAnotherBombWithinExplosionRange(bomb, anotherBomb):
                    if self.isAnotherBombBehindTheWall(bomb, anotherBomb):
                        shouldAnotherBombExplode = False
                    else:
                        shouldAnotherBombExplode = True
        return shouldAnotherBombExplode

    def updateBombs(self):
        for bomb in self.everyPlayersBombs:
            if bomb.timer > THIRD_BOMB_STATE:
                bomb.explodeBomb()
            elif self.didBombHitAnotherBomb(bomb) is True:
                bomb.explodeBomb()
            if bomb.timer < FOURTH_BOMB_STATE:
                bomb.timer += 1
            else:
                self.everyPlayersBombs.remove(bomb)

    def updateMyBombs(self):
        for bomb in self.myBombs:
            if (bomb.timer > THIRD_BOMB_STATE or self.didBombHitAnotherBomb(bomb) is True) and bomb.isExploded is False:
                bomb.isExploded = True
                bomb.timer = THIRD_BOMB_STATE + 1
            if bomb.timer < FOURTH_BOMB_STATE:
                bomb.timer += 1
            else:
                self.myBombs.remove(bomb)
                self.myBombsPlanted -= 1


