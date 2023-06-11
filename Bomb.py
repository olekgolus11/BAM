import pygame

from Map.MapClient import MapClient
from constants import *
from utilities import getTileCoordinates, Direction


class Bomb:
    def __init__(self, x, y, bombRange):
        self.map = None
        self.x = x
        self.y = y
        self.range = bombRange
        self.timer = 0
        self.isExploded = False
        self.explosionSpreadLeft = True
        self.explosionSpreadUp = True
        self.explosionSpreadDown = True
        self.explosionSpreadRight = True
        self.sound = pygame.mixer.Sound("assets/sounds/explosion.mp3")

    def explodeBomb(self):
        if self.isExploded is False:
            self.sound.play()
            self.timer = THIRD_BOMB_STATE + 1
            self.isExploded = True
            self.destroyCrates()

    def draw(self, win, map: MapClient):
        self.map = map
        self.drawBomb(win)
        if self.timer > THIRD_BOMB_STATE:
            self.drawExplosion(win)

    def drawBomb(self, win):
        bombImage = self.getBombImage()
        tileY, tileX = getTileCoordinates(self.y, self.x)
        img = pygame.image.load(bombImage)
        win.blit(img, (tileX * TILE_SIZE, tileY * TILE_SIZE))

    def drawExplosion(self, win):
        tileY, tileX = getTileCoordinates(self.y, self.x)
        img = pygame.image.load(FIRE_IMAGE)

        lastTileOnLeft = self.getLastTileInDirection(Direction.LEFT)
        lastTileOnRight = self.getLastTileInDirection(Direction.RIGHT)
        lastTileOnTop = self.getLastTileInDirection(Direction.UP)
        lastTileOnBottom = self.getLastTileInDirection(Direction.DOWN)

        for i in range(lastTileOnLeft, lastTileOnRight + 1):
            win.blit(img, (i * TILE_SIZE, tileY * TILE_SIZE))
        for i in range(lastTileOnTop, lastTileOnBottom + 1):
            win.blit(img, (tileX * TILE_SIZE, i * TILE_SIZE))

    def getLastTileInDirection(self, direction: Direction):
        tileY, tileX = getTileCoordinates(self.y, self.x)
        if direction is Direction.LEFT:
            for i in range(1, self.range):
                if self.map.isTileAWall(tileY, tileX - i):
                    return tileX - i + 1
            return tileX - self.range + 1
        elif direction is Direction.RIGHT:
            for i in range(1, self.range):
                if self.map.isTileAWall(tileY, tileX + i):
                    return tileX + i - 1
            return tileX + self.range - 1
        elif direction is Direction.UP:
            for i in range(1, self.range):
                if self.map.isTileAWall(tileY - i, tileX):
                    return tileY - i + 1
            return tileY - self.range + 1
        elif direction is Direction.DOWN:
            for i in range(1, self.range):
                if self.map.isTileAWall(tileY + i, tileX):
                    return tileY + i - 1
            return tileY + self.range - 1

    def destroyCrates(self):
        tileY, tileX = getTileCoordinates(self.y, self.x)
        lastTileOnLeft = self.getLastTileInDirection(Direction.LEFT)
        lastTileOnRight = self.getLastTileInDirection(Direction.RIGHT)
        lastTileOnTop = self.getLastTileInDirection(Direction.UP)
        lastTileOnBottom = self.getLastTileInDirection(Direction.DOWN)

        for i in range(lastTileOnLeft, lastTileOnRight + 1):
            if self.map.isTileACrate(tileY, i):
                self.map.destroyCrate(tileY, i)
        for i in range(lastTileOnTop, lastTileOnBottom + 1):
            if self.map.isTileACrate(i, tileX):
                self.map.destroyCrate(i, tileX)

    def getBombImage(self):
        if self.timer <= FIRST_BOMB_STATE:
            return BOMB_IMAGE_1
        elif self.timer <= SECOND_BOMB_STATE:
            return BOMB_IMAGE_2
        elif self.timer <= THIRD_BOMB_STATE:
            return BOMB_IMAGE_3
        elif self.timer <= FOURTH_BOMB_STATE:
            return FIRE_IMAGE


