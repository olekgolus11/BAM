import pygame


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3
        self.state = 0
        self.characterImg = 'assets/player/char1_front_standing.png'

    def draw(self, win):
        img = pygame.image.load(self.characterImg)
        win.blit(img, (self.x, self.y))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            if self.state >= 0 and self.state < 10:
                self.characterImg = 'assets/player/char1_left_standing.png'
                self.state += 1
            elif self.state >= 10 and self.state < 20:
                self.characterImg = 'assets/player/char1_left_running.png'
                self.state += 1
            else:
                self.state = 0

        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
            if self.state >= 0 and self.state < 10:
                self.characterImg = 'assets/player/char1_right_standing.png'
                self.state += 1
            elif self.state >= 10 and self.state < 20:
                self.characterImg = 'assets/player/char1_right_running.png'
                self.state += 1
            else:
                self.state = 0

        if keys[pygame.K_UP]:
            self.y -= self.speed
            if self.state >= 0 and self.state < 10:
                self.characterImg = 'assets/player/char1_back_standing.png'
                self.state += 1
            elif self.state >= 10 and self.state < 20:
                self.characterImg = 'assets/player/char1_back_running_1.png'
                self.state += 1
            elif self.state >= 20 and self.state < 30:
                self.characterImg = 'assets/player/char1_back_standing.png'
                self.state += 1
            elif self.state >= 30 and self.state < 40:
                self.characterImg = 'assets/player/char1_back_running_2.png'
                self.state += 1
            elif self.state >= 40:
                self.state = 0

        elif keys[pygame.K_DOWN]:
            self.y += self.speed
            if self.state >= 0 and self.state < 10:
                self.characterImg = 'assets/player/char1_front_standing.png'
                self.state += 1
            elif self.state >= 10 and self.state < 20:
                self.characterImg = 'assets/player/char1_front_running_1.png'
                self.state += 1
            elif self.state >= 20 and self.state < 30:
                self.characterImg = 'assets/player/char1_front_standing.png'
                self.state += 1
            elif self.state >= 30 and self.state < 40:
                self.characterImg = 'assets/player/char1_front_running_2.png'
                self.state += 1
            elif self.state >= 40:
                self.state = 0

