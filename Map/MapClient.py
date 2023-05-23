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

    def isNextTileAWall(self, y, x, keyPressed):
        if keyPressed[pygame.K_LEFT]:
            return self.board[y][x - 1] == 1 or self.board[y][x - 1] == 1.5
        elif keyPressed[pygame.K_RIGHT]:
            return self.board[y][x + 1] == 1 or self.board[y][x + 1] == 1.5
        elif keyPressed[pygame.K_UP]:
            return self.board[y - 1][x] == 1 or self.board[y - 1][x] == 1.5
        elif keyPressed[pygame.K_DOWN]:
            return self.board[y + 1][x] == 1 or self.board[y + 1][x] == 1.5
        else:
            return False

    def isNextTileACrate(self, y, x, keyPressed):
        if keyPressed[pygame.K_LEFT]:
            return self.board[y][x - 1] == 2
        elif keyPressed[pygame.K_RIGHT]:
            return self.board[y][x + 1] == 2
        elif keyPressed[pygame.K_UP]:
            return self.board[y - 1][x] == 2
        elif keyPressed[pygame.K_DOWN]:
            return self.board[y + 1][x] == 2
        else:
            return False

    def isNextTileAFloor(self, y, x, keyPressed):
        if keyPressed[pygame.K_LEFT]:
            return self.board[y][x - 1] == 0
        elif keyPressed[pygame.K_RIGHT]:
            return self.board[y][x + 1] == 0
        elif keyPressed[pygame.K_UP]:
            return self.board[y - 1][x] == 0
        elif keyPressed[pygame.K_DOWN]:
            return self.board[y + 1][x] == 0
        else:
            return False

