import random

import pygame
from Map.Map import Map
from utilities import Direction
from constants import *


class MapClient(Map):
    FLOOR = pygame.image.load("assets/blocks/floor.png")
    WALL = pygame.image.load("assets/blocks/wall.png")
    TOP_WALL = pygame.image.load("assets/blocks/top_wall.png")
    CRATE = pygame.image.load("assets/blocks/crate.png")
    MORE_BOMBS = pygame.image.load("assets/power_ups/more_bombs.png")
    MORE_POWER = pygame.image.load("assets/power_ups/more_power.png")

    def __init__(self, screen):
        self.screen = screen

    def updateBoard(self, board):
        self.board = board

    def getBlock(self, y, x):
        tileValue = self.board[y][x]
        if tileValue == 0:
            return self.FLOOR
        elif tileValue == 1:
            return self.CRATE
        elif tileValue == 2:
            return self.MORE_BOMBS
        elif tileValue == 3:
            return self.MORE_POWER
        elif tileValue == 4:
            return self.WALL
        else:
            return self.TOP_WALL

    def draw(self):
        for row in range(self.HEIGHT):
            for col in range(self.WIDTH):
                block = self.getBlock(row, col)
                if block == self.MORE_POWER or block == self.MORE_BOMBS:
                    self.screen.blit(self.FLOOR, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))
                    self.screen.blit(block, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))
                else:
                    self.screen.blit(block, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))

    def isNextTileAWall(self, y, x, direction: Direction):
        if direction == Direction.LEFT:
            return self.board[y][x - 1] >= 4
        elif direction == Direction.RIGHT:
            return self.board[y][x + 1] >= 4
        elif direction == Direction.UP:
            return self.board[y - 1][x] >= 4
        elif direction == Direction.DOWN:
            return self.board[y + 1][x] >= 4
        else:
            return False

    def isNextTileACrate(self, y, x, direction: Direction):
        if direction == Direction.LEFT:
            return self.board[y][x - 1] == 1
        elif direction == Direction.RIGHT:
            return self.board[y][x + 1] == 1
        elif direction == Direction.UP:
            return self.board[y - 1][x] == 1
        elif direction == Direction.DOWN:
            return self.board[y + 1][x] == 1
        else:
            return False

    def isNextTileAFloor(self, y, x, direction: Direction):
        if direction == Direction.LEFT:
            return self.board[y][x - 1] == 0
        elif direction == Direction.RIGHT:
            return self.board[y][x + 1] == 0
        elif direction == Direction.UP:
            return self.board[y - 1][x] == 0
        elif direction == Direction.DOWN:
            return self.board[y + 1][x] == 0
        else:
            return False

    def isNextTileABlock(self, y, x, direction: Direction):
        return self.isNextTileAWall(y, x, direction) or self.isNextTileACrate(y, x, direction)

    def isTileAWall(self, y, x):
        return self.board[y][x] >= 4

    def isTileACrate(self, y, x):
        return self.board[y][x] == 1

    def destroyCrate(self, y, x):
        self.board[y][x] = self.dropLootFromCrate()

    def dropLootFromCrate(self):
        spawn = random.randint(1, 100)
        if spawn <= 50:
            return FLOOR
        elif 50 < spawn <= 75:
            return MORE_BOMBS
        else:
            return MORE_POWER
