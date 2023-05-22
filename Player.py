import pygame
from enum import Enum


# class syntax
class Direction(Enum):
    UP = 'back'
    DOWN = 'front'
    LEFT = 'left'
    RIGHT = 'right'


class MoveState(Enum):
    STANDING = 'standing'
    RUNNING = 'running'


class Player:
    playerDirection = Direction.DOWN
    playerMoveState = MoveState.STANDING
    playerMoveFrame = None

    def __init__(self, x, y, playerId):
        self.playerId = playerId
        self.x = x
        self.y = y
        self.speed = 3
        self.state = 0

    def getImagePath(self, direction, moveState, frame=None):
        relativePath = "assets/player/char" + str(self.playerId) + "_"
        framePath = ""
        if frame:
            framePath = "_" + str(frame)
        return relativePath + direction.value + "_" + moveState.value + framePath + ".png"

    def getImageFromPath(self, path):
        return pygame.image.load(path)

    def draw(self, win):
        imagePath = self.getImagePath(self.playerDirection, self.playerMoveState, self.playerMoveFrame)
        img = self.getImageFromPath(imagePath)
        win.blit(img, (self.x, self.y))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.playerDirection = Direction.LEFT
            if self.state >= 0 and self.state < 10:
                self.playerMoveState = MoveState.STANDING
                self.playerMoveFrame = None
                self.state += 1
            elif self.state >= 10 and self.state < 20:
                self.playerMoveState = MoveState.RUNNING
                self.playerMoveFrame = None
                self.state += 1
            else:
                self.playerMoveState = MoveState.STANDING
                self.playerMoveFrame = None
                self.state = 0

        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.playerDirection = Direction.RIGHT
            if self.state >= 0 and self.state < 10:
                self.playerMoveState = MoveState.STANDING
                self.playerMoveFrame = None
                self.state += 1
            elif self.state >= 10 and self.state < 20:
                self.playerMoveState = MoveState.RUNNING
                self.playerMoveFrame = None
                self.state += 1
            else:
                self.playerMoveState = MoveState.STANDING
                self.playerMoveFrame = None
                self.state = 0

        if keys[pygame.K_UP]:
            self.y -= self.speed
            self.playerDirection = Direction.UP
            if self.state >= 0 and self.state < 10:
                self.playerMoveState = MoveState.STANDING
                self.playerMoveFrame = None
                self.state += 1
            elif self.state >= 10 and self.state < 20:
                self.playerMoveState = MoveState.RUNNING
                self.playerMoveFrame = 1
                self.state += 1
            elif self.state >= 20 and self.state < 30:
                self.playerMoveState = MoveState.STANDING
                self.playerMoveFrame = None
                self.state += 1
            elif self.state >= 30 and self.state < 40:
                self.playerMoveState = MoveState.RUNNING
                self.playerMoveFrame = 2
                self.state += 1
            elif self.state >= 40:
                self.playerMoveState = MoveState.STANDING
                self.playerMoveFrame = None
                self.state = 0

        elif keys[pygame.K_DOWN]:
            self.y += self.speed
            self.playerDirection = Direction.DOWN
            if self.state >= 0 and self.state < 10:
                self.playerMoveState = MoveState.STANDING
                self.playerMoveFrame = None
                self.state += 1
            elif self.state >= 10 and self.state < 20:
                self.playerMoveState = MoveState.RUNNING
                self.playerMoveFrame = 1
                self.state += 1
            elif self.state >= 20 and self.state < 30:
                self.playerMoveState = MoveState.STANDING
                self.playerMoveFrame = None
                self.state += 1
            elif self.state >= 30 and self.state < 40:
                self.playerMoveState = MoveState.RUNNING
                self.playerMoveFrame = 2
                self.state += 1
            elif self.state >= 40:
                self.playerMoveState = MoveState.STANDING
                self.playerMoveFrame = None
                self.state = 0
