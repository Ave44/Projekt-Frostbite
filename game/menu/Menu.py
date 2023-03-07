import pygame

from config import BUTTON_FONT


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(BUTTON_FONT, 100)
        self.menuOptionFont = pygame.font.Font(BUTTON_FONT, 75)

    def createBackground(self) -> None:
        # TODO: This is suboptimal. If possible replace this loop with a full background image intended for menu.
        background = pygame.image.load("graphics/tiles/walkable/grassland/grassland.png")
        self.screen.fill((255, 255, 255))
        screenWidth, screenHeight = self.screen.get_size()
        imageWidth, imageHeight = background.get_size()

        for x in range(0, screenWidth, imageWidth):
            for y in range(0, screenHeight, imageHeight):
                self.screen.blit(background, (x, y))

    def menuLoop(self, menuText, menuRect, menuButtons) -> None:
        while True:
            mousePos = pygame.mouse.get_pos()
            self.screen.blit(menuText, menuRect)

            for button in menuButtons:
                button.update(self.screen, mousePos)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in menuButtons:
                        if button.checkForInput(mousePos):
                            button.executeAction()

            pygame.display.update()
