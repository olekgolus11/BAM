import pygame
from Map.Map import Map


class MapClient(Map):
    FLOOR = pygame.image.load("assets/blocks/floor.png")
    WALL = pygame.image.load("assets/blocks/wall.png")
    TOP_WALL = pygame.image.load("assets/blocks/top_wall.png")
    CRATE = pygame.image.load("assets/blocks/crate.png")

    def __init__(self, screen):
        self.screen = screen

    def updateBoard(self, board):
        self.board = board

    def getBlock(self, y, x):
        tileValue = self.board[y][x]
        if tileValue == 0:
            return self.FLOOR
        elif tileValue == 1:
            return self.WALL
        elif tileValue == 1.5:
            return self.TOP_WALL
        else:
            return self.CRATE

    def draw(self):
        for row in range(self.HEIGHT):
            for col in range(self.WIDTH):
                self.screen.blit(self.getBlock(row, col), (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))
