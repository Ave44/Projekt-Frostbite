class Button:
    def __init__(self, pos, textInput, font, baseColor, hoveringColor, action, image=None):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.baseColor, self.hoveringColor = baseColor, hoveringColor
        self.textInput = textInput
        self.text = self.font.render(self.textInput, True, self.baseColor)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.action = action

    def update(self, screen, mousePos) -> None:
        self.drawText(mousePos)
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, mousePos) -> bool:
        if self.rect.collidepoint(mousePos):
            return True
        return False

    def executeAction(self):
        self.action()

    def drawText(self, mousePos) -> None:
        if self.rect.collidepoint(mousePos):
            self.text = self.font.render(self.textInput, True, self.hoveringColor)
        else:
            self.text = self.font.render(self.textInput, True, self.baseColor)
