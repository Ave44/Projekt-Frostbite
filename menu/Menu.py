from pygame import Surface, display
from pygame.image import load

from menu.general.Button import Button
from menu.general.Text import Text


class Menu:
    def __init__(self):
        self.background: Surface
        self.createBackground()
        self.buttons: list[Button] = []
        self.texts: list[Text] = []

    def createBackground(self) -> None:
        screenWidth, screenHeight = display.get_surface().get_size()
        background = Surface([screenWidth, screenHeight])
        backgroundTile = load("graphics/tiles/walkable/medow/medow.png").convert_alpha()
        imageWidth, imageHeight = backgroundTile.get_size()

        for x in range(0, screenWidth, imageWidth):
            for y in range(0, screenHeight, imageHeight):
                background.blit(backgroundTile, (x, y))

        self.background = background

    def createButtons(self) -> None:
        pass

    def createTexts(self) -> None:
        pass

    def reinitializeMenu(self):
        self.createButtons()
        self.createTexts()
        self.createBackground()
