class Button:
    def __init__(self, pos, textInput, font, baseColor, hoveringColor):
        self.x = pos[0]
        self.y = pos[1]
        self.font = font
        self.baseColor, self.hoveringColor = baseColor, hoveringColor
        self.textInput = textInput
        self.text = self.font.render(self.textInput, True, self.baseColor)
        self.textRect = self.text.get_rect(center=(self.x, self.y))

    def update(self, screen):
        screen.blit(self.text, self.textRect)

    def checkForInput(self, position):
        if position[0] in range(self.textRect.left, self.textRect.right) \
                and position[1] in range(self.textRect.top, self.textRect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.textRect.left, self.textRect.right) \
                and position[1] in range(self.textRect.top, self.textRect.bottom):
            self.text = self.font.render(self.textInput, True, self.hoveringColor)
        else:
            self.text = self.font.render(self.textInput, True, self.baseColor)
