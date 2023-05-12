import json
from os.path import isfile

from constants import FONT_MENU_COLOR
from Config import Config
from game.Game import Game
from menu.Menu import Menu
from menu.CreateGame import CreateGame
from menu.general.Button import Button


class SaveSelectMenu(Menu):
    def __init__(self, screen, config: Config, backAction):
        Menu.__init__(self, screen)
        self.config = config
        self.backAction = backAction
        self.createGameMenu = CreateGame(screen, self.initiateView, self.config)

    def loadSavefile(self, savefileName: str) -> None:
        self.config.savefileName = savefileName

        if isfile(f"./savefiles/{savefileName}.json"):
            with open(f"./savefiles/{savefileName}.json") as savefile:
                saveData = json.load(savefile)
            game = Game(self.screen, self.config, saveData)
            game.play()
        else:
            self.createGameMenu.initiateCreateGame()

        

    def createButtons(self) -> list[Button]:
        playButton = Button(pos=(0.5 * self.config.WINDOW_WIDTH, 0.347 * self.config.WINDOW_HEIGHT),
                            textInput="SAVEFILE 1",
                            font=self.config.fontBig,
                            action=self.loadSavefile,
                            actionArgument="savefile1")
        createGameButton = Button(pos=(0.5 * self.config.WINDOW_WIDTH, 0.486 * self.config.WINDOW_HEIGHT),
                                  textInput="SAVEFILE 2",
                                  font=self.config.fontBig,
                                  action=self.loadSavefile,
                            actionArgument="savefile2")
        optionsButton = Button(pos=(0.5 * self.config.WINDOW_WIDTH, 0.625 * self.config.WINDOW_HEIGHT),
                               textInput="SAVEFILE 3",
                               font=self.config.fontBig,
                               action=self.loadSavefile,
                            actionArgument="savefile3")
        quitButton = Button(pos=(0.5 * self.config.WINDOW_WIDTH, 0.764 * self.config.WINDOW_HEIGHT),
                            textInput="BACK",
                            font=self.config.fontBig,
                            action=self.backAction)
        return [playButton, optionsButton, quitButton, createGameButton]


    def initiateView(self) -> None:
        self.createBackground()
        menuText = self.config.fontHuge.render("SELECT SAVEFILE", True, FONT_MENU_COLOR)
        menuRect = menuText.get_rect(center=(0.5 * self.config.WINDOW_WIDTH, 0.138 * self.config.WINDOW_HEIGHT))

        menuButtons = self.createButtons()
        menuTexts = [[menuText, menuRect]]

        self.menuLoop(menuTexts, menuButtons)
