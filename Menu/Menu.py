import pygame
from Menu.Button import Button
from constants import *
from utilities import MenuState
from utilities import getFont
import sys


class Menu:
    screen = None
    clock = None
    playersLobbyDraw = [False, False, False]
    rulesTextArray = ["Each player starts with the same amount of bombs (1)",
                      "Each player places a bomb in order to destroy crates from which items drop,",
                      "and to kill other players",
                      "Items dropped from crates include powerups for speed, bomb range, and bomb count",
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

    def drawMenuText(self):
        menuText = getFont(125).render("BAM", True, "green")
        menuRect = menuText.get_rect(center=(CENTER_X_POS, 100))

        self.screen.blit(menuText, menuRect)

    def drawPlayersTexts(self):
        playerOneText = getFont(PLAYER_FONT_SIZE).render("Player 1", True, "black")
        playerOneRect = playerOneText.get_rect(center=(PLAYER_ONE_X_POS, PLAYER_TEXT_Y_POS))

        playerTwoText = getFont(PLAYER_FONT_SIZE).render("Player 2", True, "black")
        playerTwoRect = playerOneText.get_rect(center=(PLAYER_TWO_X_POS, PLAYER_TEXT_Y_POS))

        playerThreeText = getFont(PLAYER_FONT_SIZE).render("Player 3", True, "black")
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
        rulesText = getFont(75).render("RULES", True, "white")
        rulesRect = rulesText.get_rect(center=(CENTER_X_POS, 250))

        self.screen.blit(rulesText, rulesRect)

    def drawBackgroundRectangle(self):
        pygame.draw.rect(self.screen, "purple", pygame.Rect(CENTER_X_POS - RULES_RECTANGLE_WIDTH / 2, 180,
                                                            RULES_RECTANGLE_WIDTH, RULES_RECTANGLE_HEIGHT), 0, 30)

    def drawRulesText(self):
        for i in range(0, len(self.rulesTextArray)):
            ruleText = getFont(13).render(self.rulesTextArray[i], True, "white")
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

            backButton = Button(pos=(CENTER_X_POS, 640), textInput="BACK", font=getFont(50),
                                baseColor="white", hoveringColor="red")

            backButton.changeColor(mousePos)
            backButton.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
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

    def showLobbyBackground(self):
        self.drawBackground()
        self.drawMenuText()

        self.drawPlayersTexts()
        self.drawCircles()
        self.drawAllPlayersInLobby()

    def showLobby(self):
        self.showLobbyBackground()
        mousePos = pygame.mouse.get_pos()

        backButton = Button(pos=(CENTER_X_POS, JOIN_BACK_BUTTON_Y_POS), textInput="BACK", font=getFont(50),
                            baseColor="white", hoveringColor="red")

        backButton.changeColor(mousePos)
        backButton.update(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backButton.checkForInput(mousePos):
                    return MenuState.MENU

    def drawTextField(self, textFieldRect, color):
        pygame.draw.rect(self.screen, color, textFieldRect)

    def drawInput(self, text):
        inputText = getFont(13).render(text, True, "black")
        inputRect = inputText.get_rect(center=(CENTER_X_POS, 330))
        self.screen.blit(inputText, inputRect)

    def showJoinScreen(self):
        textField = pygame.Rect(CENTER_X_POS-TEXTFIELD_WIDTH/2, TEXTFIELD_Y_POS, TEXTFIELD_WIDTH, TEXTFIELD_HEIGHT)
        input = ''
        textFieldActive = False
        joinScreenRunning = True

        joinButton = Button(pos=(CENTER_X_POS, JOIN_BACK_BUTTON_Y_POS), textInput="JOIN", font=getFont(50),
                            baseColor="white", hoveringColor="red")

        while joinScreenRunning:
            self.drawBackground()
            self.drawMenuText()

            if textFieldActive:
                textFieldColor = "green"
            else:
                textFieldColor = "purple"

            mousePos = pygame.mouse.get_pos()
            joinButton.changeColor(mousePos)
            joinButton.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if textField.collidepoint(mousePos):
                        textFieldActive = True
                    else:
                        textFieldActive = False
                        if joinButton.checkForInput(mousePos):
                            return input if input != '' else 'localhost'
                if event.type == pygame.KEYDOWN:
                    if textFieldActive:
                        if event.key == pygame.K_BACKSPACE:
                            input = input[:-1]
                        elif event.key == pygame.K_RETURN:
                            return input if input != '' else 'localhost'
                        else:
                            input += event.unicode

            self.drawTextField(textField, textFieldColor)
            self.drawInput(input)
            pygame.display.update()

    def showStats(self, playersPointsArray):
        playerOneImage = pygame.image.load(LOBBY_PLAYER_IMAGE_1)
        self.screen.blit(playerOneImage, (PLAYER_ONE_X_POS - AVATAR_PADDING, 663))

        playerTwoImage = pygame.image.load(LOBBY_PLAYER_IMAGE_2)
        self.screen.blit(playerTwoImage, (PLAYER_TWO_X_POS - AVATAR_PADDING, 663))

        playerThreeImage = pygame.image.load(LOBBY_PLAYER_IMAGE_3)
        self.screen.blit(playerThreeImage, (PLAYER_THREE_X_POS - AVATAR_PADDING, 663))

        playerOneText = getFont(25).render(str(playersPointsArray[0]), True, "white")
        playerOneRect = playerOneText.get_rect(center=(PLAYER_ONE_X_POS + 50, 690))

        self.screen.blit(playerOneText, playerOneRect)

        playerTwoText = getFont(25).render(str(playersPointsArray[1]), True, "white")
        playerTwoRect = playerTwoText.get_rect(center=(PLAYER_TWO_X_POS + 50, 690))

        self.screen.blit(playerTwoText, playerTwoRect)

        playerThreeText = getFont(25).render(str(playersPointsArray[2]), True, "white")
        playerThreeRect = playerOneText.get_rect(center=(PLAYER_THREE_X_POS + 50, 690))

        self.screen.blit(playerThreeText, playerThreeRect)

    def showCountDownTimer(self):
        start_ticks = pygame.time.get_ticks()
        runningTimer = True
        for i in range(0, len(self.playersLobbyDraw)):
            self.playersLobbyDraw[i] = True
        while runningTimer:
            self.showLobbyBackground()

            pygame.draw.circle(self.screen, "purple", (PLAYER_TWO_X_POS, COUNTER_Y_POS), CIRCLE_RADIUS, CIRCLE_RADIUS)

            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            secondsText = getFont(50).render(str(SECONDS_TO_START_GAME-int(seconds)), True, "white")
            secondsRect = secondsText.get_rect(center=(CENTER_X_POS, COUNTER_Y_POS))

            self.screen.blit(secondsText, secondsRect)

            if seconds > SECONDS_TO_START_GAME:
                runningTimer = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    def showMenu(self):
        self.drawBackground()
        self.drawMenuText()
        mousePos = pygame.mouse.get_pos()

        playButton = Button(pos=(CENTER_X_POS, 275), textInput="PLAY", font=getFont(MENU_TEXT_FONT_SIZE),
                            baseColor="purple", hoveringColor="red")

        rulesButton = Button(pos=(CENTER_X_POS, 425), textInput="RULES", font=getFont(MENU_TEXT_FONT_SIZE),
                             baseColor="purple", hoveringColor="red")

        quitButton = Button(pos=(CENTER_X_POS, 575), textInput="QUIT", font=getFont(MENU_TEXT_FONT_SIZE),
                            baseColor="purple", hoveringColor="red")

        for button in [playButton, rulesButton, quitButton]:
            button.changeColor(mousePos)
            button.update(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.checkForInput(mousePos):
                    return MenuState.LOBBY
                elif rulesButton.checkForInput(mousePos):
                    self.rules()
                elif quitButton.checkForInput(mousePos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


menu = Menu()
menu.showMenu()
