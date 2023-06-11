import pygame
import random
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
    MORE_SPEED = pygame.image.load("assets/power_ups/more_speed.png")

    def __init__(self, screen):
        self.screen = screen

    def updateBoard(self, board):
        self.board = board

    def updateSeed(self, seed):
        random.seed(seed)

    def getBlock(self, y, x):
        tileValue = self.board[y][x]
        if tileValue == FLOOR:
            return self.FLOOR
        elif tileValue == CRATE:
            return self.CRATE
        elif tileValue == MORE_BOMBS:
            return self.MORE_BOMBS
        elif tileValue == MORE_POWER:
            return self.MORE_POWER
        elif tileValue == MORE_SPEED:
            return self.MORE_SPEED
        elif tileValue == WALL:
            return self.WALL
        else:
            return self.TOP_WALL

    def draw(self):
        self.screen.fill('black')
        for row in range(self.HEIGHT):
            for col in range(self.WIDTH):
                block = self.getBlock(row, col)
                if block == self.MORE_POWER or block == self.MORE_BOMBS or block == self.MORE_SPEED:
                    self.screen.blit(self.FLOOR, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))
                    self.screen.blit(block, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))
                else:
                    self.screen.blit(block, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))

    def isNextTileAWall(self, y, x, direction: Direction):
        if direction == Direction.LEFT:
            return self.board[y][x - 1] >= WALL
        elif direction == Direction.RIGHT:
            return self.board[y][x + 1] >= WALL
        elif direction == Direction.UP:
            return self.board[y - 1][x] >= WALL
        elif direction == Direction.DOWN:
            return self.board[y + 1][x] >= WALL
        else:
            return False

    def isNextTileACrate(self, y, x, direction: Direction):
        if direction == Direction.LEFT:
            return self.board[y][x - 1] == CRATE
        elif direction == Direction.RIGHT:
            return self.board[y][x + 1] == CRATE
        elif direction == Direction.UP:
            return self.board[y - 1][x] == CRATE
        elif direction == Direction.DOWN:
            return self.board[y + 1][x] == CRATE
        else:
            return False

    def isNextTileAFloor(self, y, x, direction: Direction):
        if direction == Direction.LEFT:
            return self.board[y][x - 1] == FLOOR or (MORE_BOMBS <= self.board[y][x - 1] <= MORE_SPEED)
        elif direction == Direction.RIGHT:
            return self.board[y][x + 1] == FLOOR or (MORE_BOMBS <= self.board[y][x + 1] <= MORE_SPEED)
        elif direction == Direction.UP:
            return self.board[y - 1][x] == FLOOR or (MORE_BOMBS <= self.board[y - 1][x] <= MORE_SPEED)
        elif direction == Direction.DOWN:
            return self.board[y + 1][x] == FLOOR or (MORE_BOMBS <= self.board[y + 1][x] <= MORE_SPEED)
        else:
            return False

    def isNextTileABlock(self, y, x, direction: Direction):
        return self.isNextTileAWall(y, x, direction) or self.isNextTileACrate(y, x, direction)

    def isTileAWall(self, y, x):
        return self.board[y][x] >= WALL

    def isTileACrate(self, y, x):
        return self.board[y][x] == CRATE

    def destroyCrate(self, y, x):
        self.board[y][x] = self.dropLootFromCrate()

    def dropLootFromCrate(self):
        drop = random.randint(1, 100)
        if drop <= 75:
            return FLOOR
        elif 75 < drop <= 85:
            return MORE_BOMBS
        elif 85 < drop <= 95:
            return MORE_POWER
        else:
            return MORE_SPEED
