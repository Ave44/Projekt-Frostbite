import sys

import pygame

from config import FONT_MENU_COLOR, BASE_BUTTON_COLOR, WHITE
from game.menu.Menu import Menu
from game.menu.OptionsMenu import OptionsMenu
from game.ui.general.Button import Button


def quitGame() -> None:
    pygame.quit()
    sys.exit()


class MainMenu(Menu):
    def __init__(self, screen, playAction):
        super().__init__(screen)
        self.play = playAction
        self.optionsMenu = OptionsMenu(screen, self.mainMenu)

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

        self.menuLoop(menuText, menuRect, menuButtons)
