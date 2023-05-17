from pygame import mixer

from constants import FONT_MENU_COLOR, MENU_THEME
from Config import Config
from menu.Menu import Menu
from menu.OptionsMenu import OptionsMenu
from menu.SaveSelectMenu import SaveSelectMenu
from menu.general.Button import Button


class MainMenu(Menu):
    def __init__(self, screen, config: Config):
        Menu.__init__(self, screen)
        self.config = config
        self.optionsMenu = OptionsMenu(screen, self.mainMenu, self.config)
        self.saveSelectMenu = SaveSelectMenu(screen, config, self.mainMenu)

    def createButtons(self) -> list[Button]:
        playButton = Button(pos=(0.5 * self.config.WINDOW_WIDTH, 0.347 * self.config.WINDOW_HEIGHT),
                            textInput="PLAY",
                            font=self.config.fontBig,
                            action=self.saveSelectMenu.initiateView)
        optionsButton = Button(pos=(0.5 * self.config.WINDOW_WIDTH, 0.55 * self.config.WINDOW_HEIGHT),
                               textInput="OPTIONS",
                               font=self.config.fontBig,
                               action=self.optionsMenu.refreshMenu)
        quitButton = Button(pos=(0.5 * self.config.WINDOW_WIDTH, 0.764 * self.config.WINDOW_HEIGHT),
                            textInput="QUIT",
                            font=self.config.fontBig,
                            action=self.quitGame)
        return [playButton, optionsButton, quitButton]

    def mainMenu(self) -> None:
        mixer.music.load(MENU_THEME)
        mixer.music.play()
        self.createBackground()
        menuText = self.config.fontHuge.render("MAIN MENU", True, FONT_MENU_COLOR)
        menuRect = menuText.get_rect(center=(0.5 * self.config.WINDOW_WIDTH, 0.138 * self.config.WINDOW_HEIGHT))
        menuButtons = self.createButtons()

        self.menuLoop([[menuText, menuRect]], menuButtons)
