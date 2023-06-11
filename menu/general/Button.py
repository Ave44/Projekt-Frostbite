from constants import BASE_BUTTON_COLOR, WHITE

class Button:
    def __init__(self, pos, textInput, font, action, baseColor=BASE_BUTTON_COLOR, hoveringColor=WHITE, image=None, actionArgument=None):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.baseColor, self.hoveringColor = baseColor, hoveringColor
        self.textInput = textInput
        self.text = self.font.render(self.textInput, False, self.baseColor)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.action = action
        self.actionArgument = actionArgument

    def update(self, mousePos) -> None:
        self.setTextColor(mousePos)

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, mousePos) -> bool:
        if self.rect.collidepoint(mousePos):
            return True
        return False

    def executeAction(self):
        if self.actionArgument:
            self.action(self.actionArgument)
        else:
            self.action()

    def setTextColor(self, mousePos) -> None:
        if self.rect.collidepoint(mousePos):
            self.text = self.font.render(self.textInput, True, self.hoveringColor)
        else:
            self.text = self.font.render(self.textInput, True, self.baseColor)
