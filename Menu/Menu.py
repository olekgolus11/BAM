import pygame
import sys
from Button import Button


class Menu:
    screen = None
    clock = None

    def __init__(self):
        self.background = pygame.image.load(f"../assets/background.jpeg")
        self.prepareScreen()

    def prepareScreen(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.screen.fill('black')
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("BAM!")

    def getFont(self, size):
        return pygame.font.Font(f"../assets/font/font.ttf", size)

    def drawMenuText(self):
        menuText = self.getFont(125).render("BAM", True, "green")
        menuRect = menuText.get_rect(center=(640, 100))

        self.screen.blit(menuText, menuRect)

    def drawPlayersTexts(self):
        playerOneText = self.getFont(18).render("Player 1", True, "red")
        playerOneRect = playerOneText.get_rect(center=(240, 235))

        playerTwoText = self.getFont(18).render("Player 2", True, "red")
        playerTwoRect = playerOneText.get_rect(center=(640, 235))

        playerThreeText = self.getFont(18).render("Player 3", True, "red")
        playerThreeRect = playerOneText.get_rect(center=(1040, 235))

        self.screen.blit(playerOneText, playerOneRect)
        self.screen.blit(playerTwoText, playerTwoRect)
        self.screen.blit(playerThreeText, playerThreeRect)

    def drawCircles(self):
        pygame.draw.circle(self.screen, "gray", (640, 360), CIRCLE_RADIUS, CIRCLE_RADIUS)
        pygame.draw.circle(self.screen, "gray", (240, 360), CIRCLE_RADIUS, CIRCLE_RADIUS)
        pygame.draw.circle(self.screen, "gray", (1040, 360), CIRCLE_RADIUS, CIRCLE_RADIUS)

    def drawBackground(self):
        self.screen.blit(self.background, (0, 0))

    def lobby(self):
        while True:
            self.drawBackground()
            self.drawMenuText()

            self.drawPlayersTexts()
            self.drawCircles()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.update()

    def showMenu(self):
        while True:
            self.drawBackground()

            mousePos = pygame.mouse.get_pos()

            self.drawMenuText()

            playButton = Button(pos=(640, 275), textInput="PLAY", font=self.getFont(75), baseColor="purple",
                                hoveringColor="red")

            rulesButton = Button(pos=(640, 425), textInput="RULES", font=self.getFont(75), baseColor="purple",
                                 hoveringColor="red")

            quitButton = Button(pos=(640, 575), textInput="QUIT", font=self.getFont(75), baseColor="purple",
                                hoveringColor="red")

            for button in [playButton, rulesButton, quitButton]:
                button.changeColor(mousePos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if playButton.checkForInput(mousePos):
                        self.lobby()
                    elif rulesButton.checkForInput(mousePos):
                        rules()
                    elif quitButton.checkForInput(mousePos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()


menu = Menu()
menu.showMenu()
