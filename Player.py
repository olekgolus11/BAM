import pygame
from enum import Enum
import constants


class Direction(Enum):
    UP = 'back'
    DOWN = 'front'
    LEFT = 'left'
    RIGHT = 'right'

from BombsHandler import BombsHandler

class MoveState(Enum):
    STANDING = 'standing'
    RUNNING = 'running'


class Player:
    PLAYER_ANIMATION_SPEED_MULTIPLIER = 0.7

    playerDirection = Direction.DOWN
    playerMoveState = MoveState.STANDING
    playerRunningImagePathValue = None

    def __init__(self, x, y, playerId):
        self.playerId = playerId
        self.x = x
        self.y = y
        self.speed = 3
        self.frameState = 0
        self.fullMoveTimeframe = constants.FPS * self.PLAYER_ANIMATION_SPEED_MULTIPLIER
        self.bombsHandler = BombsHandler()


    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.frameState += 1
            self.x -= self.speed
            self.playerDirection = Direction.LEFT
        elif keys[pygame.K_RIGHT]:
            self.frameState += 1
            self.x += self.speed
            self.playerDirection = Direction.RIGHT
        if keys[pygame.K_UP]:
            self.frameState += 1
            self.y -= self.speed
            self.playerDirection = Direction.UP
        elif keys[pygame.K_DOWN]:
            self.frameState += 1
            self.y += self.speed
            self.playerDirection = Direction.DOWN
        self.updatePlayerMoveState()
        if keys[pygame.K_SPACE]:
            self.bombsHandler.addBomb(self.x, self.y)
        else:
            self.bombsHandler.isBombPlantedThisRound = False

    def draw(self, win):
        image = self.getPlayerImage()
        win.blit(image, (self.x, self.y))
        self.bombsHandler.drawBombs(win)

    def getPlayerImage(self):
        return pygame.image.load(self.getImagePath())

    def getImagePath(self):
        relativePath = f"assets/player/char{self.playerId}_"
        runningImagePathValue = f"_{self.playerRunningImagePathValue}" if self.playerRunningImagePathValue else ""
        if self.playerDirection is None or self.playerMoveState is None:
            return f"{relativePath}front_standing.png"
        else:
            return f"{relativePath}{self.playerDirection.value}_{self.playerMoveState.value}{runningImagePathValue}.png"

    def updatePlayerMoveState(self):
        if self.shouldPlayerBeInRunningState():
            self.playerMoveState = MoveState.RUNNING
            self.updatePlayerRunningImagePathValue()
        else:
            self.playerMoveState = MoveState.STANDING
            self.playerRunningImagePathValue = None
            if self.frameState >= self.fullMoveTimeframe:
                self.frameState = 0

    def shouldPlayerBeInRunningState(self):
        frame = self.fullMoveTimeframe
        if frame * 0.25 <= self.frameState < frame * 0.5 or frame * 0.75 <= self.frameState < frame:
            return True
        else:
            return False

    def updatePlayerRunningImagePathValue(self):
        frame = self.fullMoveTimeframe
        if self.playerDirection == Direction.UP or self.playerDirection == Direction.DOWN:
            self.playerRunningImagePathValue = 1 if frame * 0.25 <= self.frameState < frame * 0.5 else 2
        else:
            self.playerRunningImagePathValue = None
