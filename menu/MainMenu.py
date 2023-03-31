import json

from constants import FONT_MENU_COLOR
from Config import Config
from game.Game import Game
from menu.CreateGame import CreateGame
from menu.Menu import Menu
from menu.OptionsMenu import OptionsMenu
from game.ui.general.Button import Button


class MainMenu(Menu):
    def __init__(self, screen, config: Config):
        Menu.__init__(self, screen, config)
        self.optionsMenu = OptionsMenu(screen, config, self.mainMenu)
        self.createGameMenu = CreateGame(screen, config, self.mainMenu)

    def playGame(self) -> None:
        # loading savefile
        # (Later will be replaced with "load all savefile names", then only selected savefile will be loaded)
        fileSave = open("./savefiles/savefile1.json")
        saveData = json.load(fileSave)
        fileSave.close()

        game = Game(self.screen, self.config, saveData)
        game.play()

    def createButtons(self) -> list[Button]:
        playButton = Button(pos=(640, 250),
                            textInput="PLAY",
                            font=self.menuOptionFont,
                            action=self.playGame)
        createGameButton = Button(pos=(640, 350),
                                  textInput="CREATE GAME",
                                  font=self.menuOptionFont,
                                  action=self.createGameMenu.initiateCreateGame)
        optionsButton = Button(pos=(640, 450),
                               textInput="OPTIONS",
                               font=self.menuOptionFont,
                               action=self.optionsMenu.options)
        quitButton = Button(pos=(640, 550),
                            textInput="QUIT",
                            font=self.menuOptionFont,
                            action=self.quitGame)
        return [playButton, optionsButton, quitButton, createGameButton]

    def mainMenu(self) -> None:
        self.createBackground()
        menuText = self.font.render("MAIN MENU", True, FONT_MENU_COLOR)
        menuRect = menuText.get_rect(center=(640, 100))
        menuButtons = self.createButtons()

        self.menuLoop([[menuText, menuRect]], menuButtons)
