import pygame
from Button import Button
from constants import *


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
        menuRect = menuText.get_rect(center=(CENTER_X_POS, 100))

        self.screen.blit(menuText, menuRect)

    def drawPlayersTexts(self):
        playerOneText = self.getFont(PLAYER_FONT_SIZE).render("Player 1", True, "red")
        playerOneRect = playerOneText.get_rect(center=(PLAYER_ONE_X_POS, PLAYER_TEXT_Y_POS))

        playerTwoText = self.getFont(PLAYER_FONT_SIZE).render("Player 2", True, "red")
        playerTwoRect = playerOneText.get_rect(center=(PLAYER_TWO_X_POS, PLAYER_TEXT_Y_POS))

        playerThreeText = self.getFont(PLAYER_FONT_SIZE).render("Player 3", True, "red")
        playerThreeRect = playerOneText.get_rect(center=(PLAYER_THREE_X_POS, PLAYER_TEXT_Y_POS))

        self.screen.blit(playerOneText, playerOneRect)
        self.screen.blit(playerTwoText, playerTwoRect)
        self.screen.blit(playerThreeText, playerThreeRect)

    def drawCircles(self):
        pygame.draw.circle(self.screen, "gray", (PLAYER_ONE_X_POS, CIRCLE_Y_POS), CIRCLE_RADIUS, CIRCLE_RADIUS)
        pygame.draw.circle(self.screen, "gray", (PLAYER_TWO_X_POS, CIRCLE_Y_POS), CIRCLE_RADIUS, CIRCLE_RADIUS)
        pygame.draw.circle(self.screen, "gray", (PLAYER_THREE_X_POS, CIRCLE_Y_POS), CIRCLE_RADIUS, CIRCLE_RADIUS)

    def drawBackground(self):
        self.screen.blit(self.background, (0, 0))

    def rules(self):
        self.drawBackground()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()

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

            playButton = Button(pos=(CENTER_X_POS, 275), textInput="PLAY", font=self.getFont(MENU_TEXT_FONT_SIZE),
                                baseColor="purple", hoveringColor="red")

            rulesButton = Button(pos=(CENTER_X_POS, 425), textInput="RULES", font=self.getFont(MENU_TEXT_FONT_SIZE),
                                 baseColor="purple", hoveringColor="red")

            quitButton = Button(pos=(CENTER_X_POS, 575), textInput="QUIT", font=self.getFont(MENU_TEXT_FONT_SIZE),
                                baseColor="purple", hoveringColor="red")

            for button in [playButton, rulesButton, quitButton]:
                button.changeColor(mousePos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if playButton.checkForInput(mousePos):
                        self.lobby()
                    elif rulesButton.checkForInput(mousePos):
                        self.rules()
                    elif quitButton.checkForInput(mousePos):
                        pygame.quit()
                        exit()

            pygame.display.update()


menu = Menu()
menu.showMenu()
