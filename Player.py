import pygame
from enum import Enum
import constants
from Map.MapClient import MapClient
from constants import TILE_SIZE
from utilities import getTileCoordinates


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
        self.screen = None
        self.playerId = playerId
        self.x = x
        self.y = y
        self.speed = 3
        self.frameState = 0
        self.fullMoveTimeframe = constants.FPS * self.PLAYER_ANIMATION_SPEED_MULTIPLIER
        self.bombsHandler = BombsHandler()
        self.map = MapClient(self.screen)

    def draw(self, screen):
        self.screen = screen
        self.updatePlayerAnimationState()
        image = self.getPlayerImage()
        screen.blit(image, (self.x, self.y))

    def move(self, board):
        self.map.updateBoard(board)
        keyPressed = pygame.key.get_pressed()
        playerShouldMoveInDirection = self.getDirectionFromKey(keyPressed)
        if self.isPlayerCollidingWithBlock(keyPressed):
            # TODO: Fix collision with dead end
            playerShouldMoveInDirection = self.correctPlayerDirectionUponCollidingWithWall(keyPressed)
        self.updatePlayerPosition(playerShouldMoveInDirection)

    def isPlayerCollidingWithBlock(self, keyPressed):
        tileY, tileX = getTileCoordinates(self.y, self.x)
        if self.isNextTileABlock(keyPressed):
            return True
        elif self.map.isNextTileAFloor(tileY, tileX, keyPressed) and (
                keyPressed[pygame.K_LEFT] or keyPressed[pygame.K_RIGHT]):
            return not self.isPositionDivisibleByTileSize(self.y)
        elif self.map.isNextTileAFloor(tileY, tileX, keyPressed) and (
                keyPressed[pygame.K_UP] or keyPressed[pygame.K_DOWN]):
            return not self.isPositionDivisibleByTileSize(self.x)
        else:
            return False

    def correctPlayerDirectionUponCollidingWithWall(self, keyPressed):
        tileY, tileX = getTileCoordinates(self.y, self.x)
        if self.isNextTileABlock(keyPressed):
            if keyPressed[pygame.K_LEFT] or keyPressed[pygame.K_RIGHT]:
                return Direction.DOWN if self.isPositionedMoreDownThanUp() else Direction.UP
            elif keyPressed[pygame.K_UP] or keyPressed[pygame.K_DOWN]:
                return Direction.RIGHT if self.isPositionedMoreRightThanLeft() else Direction.LEFT
        if self.map.isNextTileAFloor(tileY, tileX, keyPressed):
            if keyPressed[pygame.K_LEFT] or keyPressed[pygame.K_RIGHT]:
                return Direction.UP if self.isPositionedMoreDownThanUp() else Direction.DOWN
            elif keyPressed[pygame.K_UP] or keyPressed[pygame.K_DOWN]:
                return Direction.LEFT if self.isPositionedMoreRightThanLeft() else Direction.RIGHT

    def updatePlayerPosition(self, direction):
        if direction is Direction.LEFT:
            self.x -= self.speed
            self.playerDirection = Direction.LEFT
            self.frameState += 1
        elif direction is Direction.RIGHT:
            self.x += self.speed
            self.playerDirection = Direction.RIGHT
            self.frameState += 1
        elif direction is Direction.UP:
            self.y -= self.speed
            self.playerDirection = Direction.UP
            self.frameState += 1
        elif direction is Direction.DOWN:
            self.y += self.speed
            self.playerDirection = Direction.DOWN
            self.frameState += 1
        else:
            self.frameState = 0
        self.updatePlayerMoveState()
        if keys[pygame.K_SPACE]:
            self.bombsHandler.addBomb(self.x, self.y)
        else:
            self.bombsHandler.isBombPlantedThisRound = False

    def draw(self, win):
        image = self.getPlayerImage()
        win.blit(image, (self.x, self.y))
        self.bombsHandler.drawBombs(win)

    def getDirectionFromKey(self, keyPressed):
        if keyPressed[pygame.K_LEFT]:
            return Direction.LEFT
        elif keyPressed[pygame.K_RIGHT]:
            return Direction.RIGHT
        elif keyPressed[pygame.K_UP]:
            return Direction.UP
        elif keyPressed[pygame.K_DOWN]:
            return Direction.DOWN
        else:
            return None

    def isPositionDivisibleByTileSize(self, position):
        return position % TILE_SIZE == 0

    def isNextTileABlock(self, keyPressed):
        tileY, tileX = getTileCoordinates(self.y, self.x)
        isTileABlock = self.map.isNextTileAWall(tileY, tileX, keyPressed) or self.map.isNextTileACrate(tileY, tileX,
                                                                                                       keyPressed)
        if keyPressed[pygame.K_LEFT] and isTileABlock:
            return self.isPositionedMoreLeftThanRight()
        elif keyPressed[pygame.K_RIGHT] and isTileABlock:
            return self.isPositionedMoreRightThanLeft()
        elif keyPressed[pygame.K_UP] and isTileABlock:
            return self.isPositionedMoreUpThanDown()
        elif keyPressed[pygame.K_DOWN] and isTileABlock:
            return self.isPositionedMoreDownThanUp()
        else:
            return False

    def isPositionedMoreUpThanDown(self):
        return self.isPositionedOnFirstHalfOfTileInSelectedAxis(self.y - 1)

    def isPositionedMoreDownThanUp(self):
        return not self.isPositionedOnFirstHalfOfTileInSelectedAxis(self.y)

    def isPositionedMoreLeftThanRight(self):
        return self.isPositionedOnFirstHalfOfTileInSelectedAxis(self.x - 1)

    def isPositionedMoreRightThanLeft(self):
        return not self.isPositionedOnFirstHalfOfTileInSelectedAxis(self.x)

    def isPositionedOnFirstHalfOfTileInSelectedAxis(self, position):
        absolutePosition = (position + TILE_SIZE // 2) % TILE_SIZE
        return absolutePosition < TILE_SIZE // 2

    def getPlayerImage(self):
        return pygame.image.load(self.getImagePath())

    def getImagePath(self):
        relativePath = f"assets/player/char{self.playerId}_"
        runningImagePathValue = f"_{self.playerRunningImagePathValue}" if self.playerRunningImagePathValue else ""
        if self.playerDirection is None or self.playerMoveState is None:
            return f"{relativePath}front_standing.png"
        else:
            return f"{relativePath}{self.playerDirection.value}_{self.playerMoveState.value}{runningImagePathValue}.png"

    def updatePlayerAnimationState(self):
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
