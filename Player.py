import pygame
from enum import Enum
import contants

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
    playerRunningImagePathValue = None

    def __init__(self, x, y, playerId):
        self.playerId = playerId
        self.x = x
        self.y = y
        self.speed = 3
        self.stateFrame = 0
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.stateFrame += 1
            self.x -= self.speed
            self.playerDirection = Direction.LEFT
        elif keys[pygame.K_RIGHT]:
            self.stateFrame += 1
            self.x += self.speed
            self.playerDirection = Direction.RIGHT
        if keys[pygame.K_UP]:
            self.stateFrame += 1
            self.y -= self.speed
            self.playerDirection = Direction.UP
        elif keys[pygame.K_DOWN]:
            self.stateFrame += 1
            self.y += self.speed
            self.playerDirection = Direction.DOWN
        self.setMoveState()

    def draw(self, win):
        image = self.getPlayerImage()
        win.blit(image, (self.x, self.y))

    def getPlayerImage(self):
        return self.getImageFromPath(self.getImagePath())

    def getImagePath(self):
        relativePath = f"assets/player/char{self.playerId}_"
        runningImagePathValue = f"_{self.playerRunningImagePathValue}" if self.playerRunningImagePathValue else ""

        if self.playerDirection is None or self.playerMoveState is None:
            return f"{relativePath}front_standing.png"
        else:
            return f"{relativePath}{self.playerDirection.value}_{self.playerMoveState.value}{runningImagePathValue}.png"

    def getImageFromPath(self, path):
        return pygame.image.load(path)

    def setMoveState(self):
        if 10 <= self.stateFrame < 20 or 30 <= self.stateFrame < 40:
            self.playerMoveState = MoveState.RUNNING
            if self.playerDirection == Direction.UP or self.playerDirection == Direction.DOWN:
                self.playerRunningImagePathValue = 1 if 10 <= self.stateFrame < 20 else 2
            else:
                self.playerRunningImagePathValue = None
        else:
            self.playerMoveState = MoveState.STANDING
            self.playerRunningImagePathValue = None
            if self.stateFrame >= 40:
                self.stateFrame = 0

