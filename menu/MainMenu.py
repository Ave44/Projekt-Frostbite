import sys
from pygame import quit

from constants import FONT_MENU_COLOR
from Config import Config
from menu.Menu import Menu
from menu.general.Button import Button
from menu.general.Text import Text


class MainMenu(Menu):
    def __init__(self, config: Config, goToCreateGameMenu: callable, goToOptionsMenu: callable):
        Menu.__init__(self)
        self.config = config
        self.goToCreateGameMenu = goToCreateGameMenu
        self.goToOptionsMenu = goToOptionsMenu

        self.createButtons()
        self.createTexts()

    def createButtons(self) -> None:
        playButton = Button(pos=(0.5 * self.config.WINDOW_WIDTH, 0.347 * self.config.WINDOW_HEIGHT),
                            textInput="PLAY",
                            font=self.config.fontBig,
                            action=self.goToCreateGameMenu)
        optionsButton = Button(pos=(0.5 * self.config.WINDOW_WIDTH, 0.55 * self.config.WINDOW_HEIGHT),
                               textInput="OPTIONS",
                               font=self.config.fontBig,
                               action=self.goToOptionsMenu)
        quitButton = Button(pos=(0.5 * self.config.WINDOW_WIDTH, 0.764 * self.config.WINDOW_HEIGHT),
                            textInput="QUIT",
                            font=self.config.fontBig,
                            action=self.quitGame)
        self.buttons = [playButton, optionsButton, quitButton]

    def createTexts(self) -> None:
        mainMenuTextPos = (0.5 * self.config.WINDOW_WIDTH, 0.138 * self.config.WINDOW_HEIGHT)
        mainMenuText = Text(mainMenuTextPos, "MAIN MENU", self.config.fontHuge, FONT_MENU_COLOR)

        self.texts = [mainMenuText]

    def quitGame(self):
        quit()
        sys.exit()
