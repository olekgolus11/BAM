import pygame
import sys
from Button import Button

pygame.init()

screen = pygame.display.set_mode((1280, 720))
screen.fill('#1e1e1e')
pygame.display.set_caption("Menu")

background = pygame.image.load(f"../assets/background.jpeg")


class Menu:
    screen = None
    clock = None

    def __init__(self):
        self.prepareScreen()

    def prepareScreen(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.screen.fill('black')
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("BAM!")

    def getFont(self, size):
        return pygame.font.Font(f"../assets/font/font.ttf", size)

    def showMenu(self):
        pygame.display.set_caption("Menu")

        while True:
            self.screen.blit(background, (0, 0))

            mousePos = pygame.mouse.get_pos()

            menuText = self.getFont(125).render("BAM", True, "green")
            menuRect = menuText.get_rect(center=(640, 100))

            playButton = Button(pos=(640, 275), textInput="PLAY", font=self.getFont(75), baseColor="purple",
                                hoveringColor="red")

            rulesButton = Button(pos=(640, 425), textInput="RULES", font=self.getFont(75), baseColor="purple",
                                 hoveringColor="red")

            quitButton = Button(pos=(640, 575), textInput="QUIT", font=self.getFont(75), baseColor="purple",
                                hoveringColor="red")

            self.screen.blit(menuText, menuRect)

            for button in [playButton, rulesButton, quitButton]:
                button.changeColor(mousePos)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if playButton.checkForInput(mousePos):
                        lobby()
                    elif rulesButton.checkForInput(mousePos):
                        rules()
                    elif quitButton.checkForInput(mousePos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()


menu = Menu()
menu.showMenu()
