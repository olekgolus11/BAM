import pygame
from BombsHandler import BombsHandler
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
        self.bombsHandler = BombsHandler()
        self.characterImg = self.CHAR_FRONT_STANDING

    def createImages(self):
        self.CHAR_FRONT_STANDING = "assets/player/char" + str(self.playerId) + "_front_standing.png"
        self.CHAR_FRONT_RUNNING_1 = "assets/player/char" + str(self.playerId) + "_front_running_1.png"
        self.CHAR_FRONT_RUNNING_2 = "assets/player/char" + str(self.playerId) + "_front_running_2.png"

        self.CHAR_BACK_STANDING = "assets/player/char" + str(self.playerId) + "_back_standing.png"
        self.CHAR_BACK_RUNNING_1 = "assets/player/char" + str(self.playerId) + "_back_running_1.png"
        self.CHAR_BACK_RUNNING_2 = "assets/player/char" + str(self.playerId) + "_back_running_2.png"

        self.CHAR_LEFT_STANDING = "assets/player/char" + str(self.playerId) + "_left_standing.png"
        self.CHAR_LEFT_RUNNING = "assets/player/char" + str(self.playerId) + "_left_running.png"

        self.CHAR_RIGHT_STANDING = "assets/player/char" + str(self.playerId) + "_right_standing.png"
        self.CHAR_RIGHT_RUNNING = "assets/player/char" + str(self.playerId) + "_right_running.png"

    def draw(self, win):
        img = pygame.image.load(self.characterImg)
        win.blit(img, (self.x, self.y))
        self.bombsHandler.printBombs(win)

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

        if keys[pygame.K_SPACE]:
            self.bombsHandler.addBomb(self.x, self.y)
        else:
            self.bombsHandler.isBombPlantedThisRound = False




