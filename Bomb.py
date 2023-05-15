import pygame
from constants import *

class Bomb:
    def __init__(self, x, y, power):
        self.x = x
        self.y = y
        self.power = power
        self.timer = 0

    def __del__(self):
        pass

    def plant(self, win):
        file = 0
        if self.timer <= FIRST_BOMB_STATE:
            file = BOMB_IMAGE_1
        elif self.timer <= SECOND_BOMB_STATE:
            file = BOMB_IMAGE_2
        elif self.timer <= THIRD_BOMB_STATE:
            file = BOMB_IMAGE_3
        elif self.timer <= FOURTH_BOMB_STATE:
            file = FIRE_IMAGE
        else:
            return

        img = pygame.image.load(file)
        win.blit(img, (self.x, self.y))

        if self.timer > THIRD_BOMB_STATE:
            for i in range(0, self.power):
                win.blit(img, (self.x, self.y + BOMB_HEIGHT * i))
                win.blit(img, (self.x, self.y - BOMB_HEIGHT * i))
                win.blit(img, (self.x + BOMB_WIDTH * i, self.y))
                win.blit(img, (self.x - BOMB_WIDTH * i, self.y))

        self.timer += 1



