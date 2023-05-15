import pygame

BOMB_WIDTH = 60
BOMB_HEIGHT = 60
FIRST_BOMB_STATE = 40
SECOND_BOMB_STATE = 80
THIRD_BOMB_STATE = 120
FOURTH_BOMB_STATE = 160

BOMB_IMAGE_1 = 'assets/bomb/bomb1.png'
BOMB_IMAGE_2 = 'assets/bomb/bomb2.png'
BOMB_IMAGE_3 = 'assets/bomb/bomb3.png'
FIRE_IMAGE = 'assets/bomb/fire.png'

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



