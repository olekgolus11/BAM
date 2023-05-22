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
    CHAR_FRONT_STANDING = None
    CHAR_FRONT_RUNNING_1 = None
    CHAR_FRONT_RUNNING_2 = None

    CHAR_BACK_STANDING = None
    CHAR_BACK_RUNNING_1 = None
    CHAR_BACK_RUNNING_2 = None

    CHAR_LEFT_STANDING = None
    CHAR_LEFT_RUNNING = None

    CHAR_RIGHT_STANDING = None
    CHAR_RIGHT_RUNNING = None

    def __init__(self, x, y, playerId):
        self.playerId = playerId
        self.x = x
        self.y = y
        self.speed = 3
        self.state = 0
        self.createImages()
        self.characterImg = self.CHAR_FRONT_STANDING

    def getImagePath(self, direction, moveState, frame=None):
        relativePath = "assets/player/char" + str(self.playerId) + "_"
        framePath = ""
        if frame:
            framePath = "_" + str(frame)
        return relativePath + direction.value + "_" + moveState.value + framePath + ".png"

    def createImages(self):
        self.CHAR_FRONT_STANDING = self.getImagePath(Direction.DOWN, MoveState.STANDING)
        self.CHAR_FRONT_RUNNING_1 = self.getImagePath(Direction.DOWN, MoveState.RUNNING, 1)
        self.CHAR_FRONT_RUNNING_2 = self.getImagePath(Direction.DOWN, MoveState.RUNNING, 2)

        self.CHAR_BACK_STANDING = self.getImagePath(Direction.UP, MoveState.STANDING)
        self.CHAR_BACK_RUNNING_1 = self.getImagePath(Direction.UP, MoveState.RUNNING, 1)
        self.CHAR_BACK_RUNNING_2 = self.getImagePath(Direction.UP, MoveState.RUNNING, 2)

        self.CHAR_LEFT_STANDING = self.getImagePath(Direction.LEFT, MoveState.STANDING)
        self.CHAR_LEFT_RUNNING = self.getImagePath(Direction.LEFT, MoveState.RUNNING)

        self.CHAR_RIGHT_STANDING = self.getImagePath(Direction.RIGHT, MoveState.STANDING)
        self.CHAR_RIGHT_RUNNING = self.getImagePath(Direction.RIGHT, MoveState.RUNNING)

    def draw(self, win):
        img = pygame.image.load(self.characterImg)
        win.blit(img, (self.x, self.y))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            if self.state >= 0 and self.state < 10:
                self.characterImg = self.CHAR_LEFT_STANDING
                self.state += 1
            elif self.state >= 10 and self.state < 20:
                self.characterImg = self.CHAR_LEFT_RUNNING
                self.state += 1
            else:
                self.state = 0

        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
            if self.state >= 0 and self.state < 10:
                self.characterImg = self.CHAR_RIGHT_STANDING
                self.state += 1
            elif self.state >= 10 and self.state < 20:
                self.characterImg = self.CHAR_RIGHT_RUNNING
                self.state += 1
            else:
                self.state = 0

        if keys[pygame.K_UP]:
            self.y -= self.speed
            if self.state >= 0 and self.state < 10:
                self.characterImg = self.CHAR_BACK_STANDING
                self.state += 1
            elif self.state >= 10 and self.state < 20:
                self.characterImg = self.CHAR_BACK_RUNNING_1
                self.state += 1
            elif self.state >= 20 and self.state < 30:
                self.characterImg = self.CHAR_BACK_STANDING
                self.state += 1
            elif self.state >= 30 and self.state < 40:
                self.characterImg = self.CHAR_BACK_RUNNING_2
                self.state += 1
            elif self.state >= 40:
                self.state = 0

        elif keys[pygame.K_DOWN]:
            self.y += self.speed
            if self.state >= 0 and self.state < 10:
                self.characterImg = self.CHAR_FRONT_STANDING
                self.state += 1
            elif self.state >= 10 and self.state < 20:
                self.characterImg = self.CHAR_FRONT_RUNNING_1
                self.state += 1
            elif self.state >= 20 and self.state < 30:
                self.characterImg = self.CHAR_FRONT_STANDING
                self.state += 1
            elif self.state >= 30 and self.state < 40:
                self.characterImg = self.CHAR_FRONT_RUNNING_2
                self.state += 1
            elif self.state >= 40:
                self.state = 0
