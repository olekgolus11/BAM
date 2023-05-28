import pygame
import constants
from Map.MapClient import MapClient
from constants import TILE_SIZE
from utilities import getTileCoordinates
from BombsHandler import BombsHandler
from utilities import Direction
from utilities import MoveState


class Player:
    PLAYER_ANIMATION_SPEED_MULTIPLIER = 0.7

    playerDirection = Direction.DOWN
    playerMoveState = MoveState.STANDING
    playerRunningImagePathValue = None

    def __init__(self, x, y, playerId, screen):
        self.screen = screen
        self.playerId = playerId
        self.x = x
        self.y = y
        self.speed = 3
        self.frameState = 0
        self.fullMoveTimeframe = constants.FPS * self.PLAYER_ANIMATION_SPEED_MULTIPLIER
        self.bombsHandler = BombsHandler()
        self.map = MapClient(self.screen)
        self.shouldPlayerMove = True

    def draw(self):
        self.updatePlayerAnimationState()
        image = self.getPlayerImage()
        self.screen.blit(image, (self.x, self.y))
        self.bombsHandler.drawBombs(self.screen)

    def run(self):
        keyPressed = pygame.key.get_pressed()
        self.handlePlayerMovement(keyPressed)
        self.handlePlayerBomb(keyPressed)

    def handlePlayerMovement(self, keyPressed):
        playerShouldMoveInDirection = self.getDirectionFromKey(keyPressed)
        self.shouldPlayerMove = True
        if self.isPlayerSurroundedWithBlocks(playerShouldMoveInDirection):
            self.shouldPlayerMove = False
        if self.isPlayerCollidingWithBlock(playerShouldMoveInDirection):
            playerShouldMoveInDirection = self.correctPlayerDirectionUponCollidingWithBlock(playerShouldMoveInDirection)
        self.updatePlayerPosition(playerShouldMoveInDirection)

    def handlePlayerBomb(self, keyPressed):
        if keyPressed[pygame.K_SPACE]:
            self.bombsHandler.addBomb(self.x, self.y)
        else:
            self.bombsHandler.isBombPlantedThisRound = False

    def isPlayerCollidingWithBlock(self, direction: Direction):
        tileY, tileX = getTileCoordinates(self.y, self.x)
        if self.isPlayerNearTheBlock(direction):
            return True
        elif self.map.isNextTileAFloor(tileY, tileX, direction) and (
                direction == Direction.LEFT or direction == Direction.RIGHT):
            return not self.isPositionDivisibleByTileSize(self.y)
        elif self.map.isNextTileAFloor(tileY, tileX, direction) and (
                direction == Direction.UP or direction == Direction.DOWN):
            return not self.isPositionDivisibleByTileSize(self.x)
        else:
            return False

    def correctPlayerDirectionUponCollidingWithBlock(self, direction: Direction):
        correctedDirection = None
        if self.isPlayerNearTheBlock(direction):
            if direction == Direction.LEFT or direction == Direction.RIGHT:
                correctedDirection = Direction.DOWN if self.isPositionedMoreDownThanUp() else Direction.UP
            elif direction == Direction.UP or direction == Direction.DOWN:
                correctedDirection = Direction.RIGHT if self.isPositionedMoreRightThanLeft() else Direction.LEFT
        else:
            if direction == Direction.LEFT or direction == Direction.RIGHT:
                correctedDirection = Direction.UP if self.isPositionedMoreDownThanUp() else Direction.DOWN
            elif direction == Direction.UP or direction == Direction.DOWN:
                correctedDirection = Direction.LEFT if self.isPositionedMoreRightThanLeft() else Direction.RIGHT
        if self.isPlayerSurroundedWithBlocks(correctedDirection):
            self.shouldPlayerMove = False
        return correctedDirection

    def updatePlayerPosition(self, direction):
        if not self.shouldPlayerMove:
            self.frameState = 0
        elif direction is Direction.LEFT:
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

    def isPlayerSurroundedWithBlocks(self, direction: Direction):
        if direction == Direction.LEFT or direction == Direction.RIGHT:
            return self.isPlayerCollidingWithBlock(direction) \
                and self.isPlayerCollidingWithBlock(Direction.UP) \
                and self.isPlayerCollidingWithBlock(Direction.DOWN)
        elif direction == Direction.UP or direction == Direction.DOWN:
            return self.isPlayerCollidingWithBlock(direction) \
                and self.isPlayerCollidingWithBlock(Direction.LEFT) \
                and self.isPlayerCollidingWithBlock(Direction.RIGHT)
        else:
            return False

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

    def isPlayerNearTheBlock(self, direction: Direction):
        tileY, tileX = getTileCoordinates(self.y, self.x)
        isTileABlock = self.map.isNextTileABlock(tileY, tileX, direction)
        if direction == Direction.LEFT and isTileABlock:
            return self.isPositionedMoreLeftThanRight()
        elif direction == Direction.RIGHT and isTileABlock:
            return self.isPositionedMoreRightThanLeft()
        elif direction == Direction.UP and isTileABlock:
            return self.isPositionedMoreUpThanDown()
        elif direction == Direction.DOWN and isTileABlock:
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
