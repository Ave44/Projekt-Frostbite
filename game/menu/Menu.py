import sys

import pygame

from config import BUTTON_FONT, FONT_MENU_COLOR, BASE_BUTTON_COLOR, WHITE
from game.menu.OptionsMenu import OptionsMenu
from game.ui.general.Button import Button


def quitGame() -> None:
    pygame.quit()
    sys.exit()


class Menu:
    def __init__(self, screen, playAction):
        self.screen = screen
        self.play = playAction
        self.font = pygame.font.Font(BUTTON_FONT, 100)
        self.menuOptionFont = pygame.font.Font(BUTTON_FONT, 75)
        self.optionsMenu = OptionsMenu(screen, self.mainMenu)

    def createBackground(self) -> None:
        # TODO: This is suboptimal. If possible replace this loop with a full background image intended for menu.
        background = pygame.image.load("graphics/tiles/walkable/grassland/grassland.png")
        self.screen.fill((255, 255, 255))
        screenWidth, screenHeight = self.screen.get_size()
        imageWidth, imageHeight = background.get_size()

        for x in range(0, screenWidth, imageWidth):
            for y in range(0, screenHeight, imageHeight):
                self.screen.blit(background, (x, y))

    def mainMenu(self) -> None:
        self.createBackground()
        menuText = self.font.render("MAIN MENU", True, FONT_MENU_COLOR)
        menuRect = menuText.get_rect(center=(640, 100))
        play_button = Button(pos=(640, 250),
                             textInput="PLAY",
                             font=self.menuOptionFont, baseColor=BASE_BUTTON_COLOR, hoveringColor=WHITE,
                             action=self.play)
        options_button = Button(pos=(640, 400),
                                textInput="OPTIONS",
                                font=self.menuOptionFont, baseColor=BASE_BUTTON_COLOR, hoveringColor=WHITE,
                                action=self.optionsMenu.options)
        quit_button = Button(pos=(640, 550),
                             textInput="QUIT",
                             font=self.menuOptionFont, baseColor=BASE_BUTTON_COLOR, hoveringColor=WHITE,
                             action=quitGame)
        menuButtons = [play_button, options_button, quit_button]

        while True:
            mousePos = pygame.mouse.get_pos()
            self.screen.blit(menuText, menuRect)

            for button in menuButtons:
                button.update(self.screen, mousePos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quitGame()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in menuButtons:
                        if button.checkForInput(mousePos):
                            button.executeAction()

            pygame.display.update()
