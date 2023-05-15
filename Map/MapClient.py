import pygame

from Map.Map import Map


class MapClient(Map):
    def __init__(self, screen):
        self.screen = screen

    def updateBoard(self, board):
        self.board = board

    def getBlock(self, y, x):
        value = self.board[y][x]
        if value == 0:
            return 'white'
        elif value == 1:
            return 'black'
        else:
            return 'red'

    def draw(self):
        for row in range(self.HEIGHT):
            for col in range(self.WIDTH):
                pygame.draw.rect(self.screen, self.getBlock(row, col), (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))
