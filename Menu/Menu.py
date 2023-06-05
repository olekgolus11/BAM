import pygame
from Menu.Button import Button
from constants import *
from utilities import MenuState


class Menu:
    screen = None
    clock = None
    playersLobbyDraw = [False, False, False]
    rulesTextArray = ["Each player starts with the same amount of bombs (3)",
                      "Each player places a bomb in order to destroy crates from which items drop,",
                      "and to kill other players",
                      "Items dropped from crates include powerups for speed, bomb range,",
                      "or temporary immunity to explosions",
                      "Each game consists of 3 players",
                      "The map consists of indestructible walls in order to make the game more interesting"]

    def __init__(self):
        self.background = pygame.image.load(f"assets/background.jpeg")
        self.prepareScreen()

    def prepareScreen(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.screen.fill('black')
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("BAM!")

    def getFont(self, size):
        return pygame.font.Font(f"assets/font/font.ttf", size)

    def drawMenuText(self):
        menuText = self.getFont(125).render("BAM", True, "green")
        menuRect = menuText.get_rect(center=(CENTER_X_POS, 100))

        self.screen.blit(menuText, menuRect)

    def drawPlayersTexts(self):
        playerOneText = self.getFont(PLAYER_FONT_SIZE).render("Player 1", True, "black")
        playerOneRect = playerOneText.get_rect(center=(PLAYER_ONE_X_POS, PLAYER_TEXT_Y_POS))

        playerTwoText = self.getFont(PLAYER_FONT_SIZE).render("Player 2", True, "black")
        playerTwoRect = playerOneText.get_rect(center=(PLAYER_TWO_X_POS, PLAYER_TEXT_Y_POS))

        playerThreeText = self.getFont(PLAYER_FONT_SIZE).render("Player 3", True, "black")
        playerThreeRect = playerOneText.get_rect(center=(PLAYER_THREE_X_POS, PLAYER_TEXT_Y_POS))

        self.screen.blit(playerOneText, playerOneRect)
        self.screen.blit(playerTwoText, playerTwoRect)
        self.screen.blit(playerThreeText, playerThreeRect)

    def drawCircles(self):
        pygame.draw.circle(self.screen, "red", (PLAYER_ONE_X_POS, CIRCLE_Y_POS), CIRCLE_RADIUS, CIRCLE_RADIUS)
        pygame.draw.circle(self.screen, "red", (PLAYER_TWO_X_POS, CIRCLE_Y_POS), CIRCLE_RADIUS, CIRCLE_RADIUS)
        pygame.draw.circle(self.screen, "red", (PLAYER_THREE_X_POS, CIRCLE_Y_POS), CIRCLE_RADIUS, CIRCLE_RADIUS)

    def drawBackground(self):
        self.screen.blit(self.background, (0, 0))

    def drawRulesMainText(self):
        rulesText = self.getFont(75).render("RULES", True, "white")
        rulesRect = rulesText.get_rect(center=(CENTER_X_POS, 250))

        self.screen.blit(rulesText, rulesRect)

    def drawBackgroundRectangle(self):
        pygame.draw.rect(self.screen, "purple", pygame.Rect(CENTER_X_POS - RULES_RECTANGLE_WIDTH / 2, 180,
                                                            RULES_RECTANGLE_WIDTH, RULES_RECTANGLE_HEIGHT), 0, 30)

    def drawRulesText(self):
        for i in range(0, len(self.rulesTextArray)):
            ruleText = self.getFont(13).render(self.rulesTextArray[i], True, "white")
            ruleRect = ruleText.get_rect(center=(CENTER_X_POS, 330 + i * 40))
            ruleRect.left = CENTER_X_POS / 6
            self.screen.blit(ruleText, ruleRect)

    def rules(self):
        while True:
            self.drawBackground()
            self.drawMenuText()
            mousePos = pygame.mouse.get_pos()

            self.drawBackgroundRectangle()
            self.drawRulesMainText()
            self.drawRulesText()

            backButton = Button(pos=(CENTER_X_POS, 640), textInput="BACK", font=self.getFont(50),
                                baseColor="white", hoveringColor="red")

            backButton.changeColor(mousePos)
            backButton.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if backButton.checkForInput(mousePos):
                        return

            pygame.display.update()

    def drawPlayerInLobby(self, playerId):
        self.playersLobbyDraw[playerId-1] = True

    def drawAllPlayersInLobby(self):
        if self.playersLobbyDraw[0]:
            playerImage = pygame.image.load(LOBBY_PLAYER_IMAGE_1)
            pygame.draw.circle(self.screen, "green", (PLAYER_ONE_X_POS, CIRCLE_Y_POS), CIRCLE_RADIUS, CIRCLE_RADIUS)
            self.screen.blit(playerImage, (PLAYER_ONE_X_POS - AVATAR_PADDING, CIRCLE_Y_POS - AVATAR_PADDING))
        if self.playersLobbyDraw[1]:
            playerImage = pygame.image.load(LOBBY_PLAYER_IMAGE_2)
            pygame.draw.circle(self.screen, "green", (PLAYER_TWO_X_POS, CIRCLE_Y_POS), CIRCLE_RADIUS, CIRCLE_RADIUS)
            self.screen.blit(playerImage, (PLAYER_TWO_X_POS - AVATAR_PADDING, CIRCLE_Y_POS - AVATAR_PADDING))
        if self.playersLobbyDraw[2]:
            playerImage = pygame.image.load(LOBBY_PLAYER_IMAGE_3)
            pygame.draw.circle(self.screen, "green", (PLAYER_THREE_X_POS, CIRCLE_Y_POS), CIRCLE_RADIUS, CIRCLE_RADIUS)
            self.screen.blit(playerImage, (PLAYER_THREE_X_POS - AVATAR_PADDING, CIRCLE_Y_POS - AVATAR_PADDING))

    def showLobby(self):
        self.drawBackground()
        self.drawMenuText()

        self.drawPlayersTexts()
        self.drawCircles()

        self.drawAllPlayersInLobby()

        pygame.display.update()

    def showCountDownTimer(self):
        start_ticks = pygame.time.get_ticks()
        runningTimer = True
        while runningTimer:
            self.drawBackground()
            self.drawMenuText()

            pygame.draw.circle(self.screen, "purple", (PLAYER_TWO_X_POS, CIRCLE_Y_POS), CIRCLE_RADIUS, CIRCLE_RADIUS)

            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            secondsText = self.getFont(50).render(str(10-int(seconds)), True, "white")
            secondsRect = secondsText.get_rect(center=(CENTER_X_POS, CIRCLE_Y_POS))

            self.screen.blit(secondsText, secondsRect)

            if seconds > 10:
                runningTimer = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.update()

    def showMenu(self):
        self.drawBackground()
        self.drawMenuText()
        mousePos = pygame.mouse.get_pos()

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
                    return MenuState.LOBBY
                elif rulesButton.checkForInput(mousePos):
                    self.rules()
                elif quitButton.checkForInput(mousePos):
                    pygame.quit()
                    exit()

        pygame.display.update()


menu = Menu()
menu.showMenu()