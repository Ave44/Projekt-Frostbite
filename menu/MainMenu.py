import json

from constants import FONT_MENU_COLOR
from Config import Config
from game.Game import Game
from menu.CreateGame import CreateGame
from menu.Menu import Menu
from menu.OptionsMenu import OptionsMenu
from menu.general.Button import Button


class MainMenu(Menu):
    def __init__(self, screen, config: Config):
        Menu.__init__(self, screen)
        self.config = config
        self.optionsMenu = OptionsMenu(screen, self.mainMenu, self.config)
        self.createGameMenu = CreateGame(screen, self.mainMenu, self.config)

    def playGame(self) -> None:
        # loading savefile
        # (Later will be replaced with "load all savefile names", then only selected savefile will be loaded)
        fileSave = open("./savefiles/savefile1.json")
        saveData = json.load(fileSave)
        fileSave.close()

        game = Game(self.screen, self.config, saveData)
        game.play()

    def createButtons(self) -> list[Button]:
        playButton = Button(pos=(0.5 * self.config.WINDOW_WIDTH, 0.347 * self.config.WINDOW_HEIGHT),
                            textInput="PLAY",
                            font=self.menuOptionFont,
                            action=self.playGame)
        createGameButton = Button(pos=(0.5 * self.config.WINDOW_WIDTH, 0.486 * self.config.WINDOW_HEIGHT),
                                  textInput="CREATE GAME",
                                  font=self.menuOptionFont,
                                  action=self.createGameMenu.initiateCreateGame)
        optionsButton = Button(pos=(0.5 * self.config.WINDOW_WIDTH, 0.625 * self.config.WINDOW_HEIGHT),
                               textInput="OPTIONS",
                               font=self.menuOptionFont,
                               action=self.optionsMenu.options)
        quitButton = Button(pos=(0.5 * self.config.WINDOW_WIDTH, 0.764 * self.config.WINDOW_HEIGHT),
                            textInput="QUIT",
                            font=self.menuOptionFont,
                            action=self.quitGame)
        return [playButton, optionsButton, quitButton, createGameButton]

    def mainMenu(self) -> None:
        self.createBackground()
        menuText = self.font.render("MAIN MENU", True, FONT_MENU_COLOR)
        menuRect = menuText.get_rect(center=(0.5 * self.config.WINDOW_WIDTH, 0.138 * self.config.WINDOW_HEIGHT))
        menuButtons = self.createButtons()

        self.menuLoop([[menuText, menuRect]], menuButtons)
