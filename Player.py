import pygame


class Player():
    def __init__(self, x, y):
        self.id = -1
        self.x = x
        self.y = y
        self.connected = 0
        self.vel = 3
        self.state = 0
        self.bombs = 2
        self.drawBomb = 0
        self.bombTime = 2000
        self.char = 'images\character_front_standing.png'

    def draw(self, win):
        img = pygame.image.load(self.char)
        win.blit(img,(self.x,self.y))

    def move(self):
        keys = pygame.key.get_pressed()
        self.char = 'images\character_front_standing.png'
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
            if self.state >= 0 and self.state < 10:
                self.char = 'images\character_left_standing.png'
                self.state += 1
            elif self.state >= 10 and self.state < 20:
                self.char = 'images\character_left_run.png'
                self.state += 1
            elif self.state >= 20 and self.state < 30:
                self.char = 'images\character_left_standing.png'
                self.state += 1
            elif self.state >= 30 and self.state < 40:
                self.char = 'images\character_left_run.png'
                self.state += 1
            elif self.state >= 40:
                self.char = 'images\character_left_standing.png'
                self.state = 0

        elif keys[pygame.K_RIGHT]:
            self.x += self.vel
            if self.state >= 0 and self.state < 10:
                self.char = 'images\character_right_standing.png'
                self.state += 1
            elif self.state >= 10 and self.state < 20:
                self.char = 'images\character_right_run.png'
                self.state += 1
            elif self.state >= 20 and self.state < 30:
                self.char = 'images\character_right_standing.png'
                self.state += 1
            elif self.state >= 30 and self.state < 40:
                self.char = 'images\character_right_run.png'
                self.state += 1
            elif self.state >= 40:
                self.char = 'images\character_right_standing.png'
                self.state = 0

        if keys[pygame.K_UP]:
            self.y -= self.vel
            if self.state >= 0 and self.state < 10:
                self.char = 'images\character_back_standing.png'
                self.state += 1
            elif self.state >= 10 and self.state < 20:
                self.char = 'images\character_back_run_1.png'
                self.state += 1
            elif self.state >= 20 and self.state < 30:
                self.char = 'images\character_back_standing.png'
                self.state += 1
            elif self.state >= 30 and self.state < 40:
                self.char = 'images\character_back_run_2.png'
                self.state += 1
            elif self.state >= 40:
                self.char = 'images\character_back_standing.png'
                self.state = 0

        elif keys[pygame.K_DOWN]:
            self.y += self.vel
            if self.state >= 0 and self.state < 10:
                self.char = 'images\character_front_standing.png'
                self.state += 1
            elif self.state >= 10 and self.state < 20:
                self.char = 'images\character_front_run_1.png'
                self.state += 1
            elif self.state >= 20 and self.state < 30:
                self.char = 'images\character_front_standing.png'
                self.state += 1
            elif self.state >= 30 and self.state < 40:
                self.char = 'images\character_front_run_2.png'
                self.state += 1
            elif self.state >= 40:
                self.char = 'images\character_front_standing.png'
                self.state = 0


        self.update()

    def update(self):
        self.rect = (self.x, self.y)