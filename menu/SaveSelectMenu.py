import json
from os import remove
from os.path import isfile
from pygame import Vector2

from constants import FONT_MENU_COLOR, DELETE_SAVEFILE_COLOR
from Config import Config
from game.Game import Game
from menu.Menu import Menu
from menu.CreateGame import CreateGame
from menu.general.Button import Button
from menu.general.LoadingScreenGenerator import LoadingScreenGenerator


class SaveSelectMenu(Menu):
    def __init__(self, screen, config: Config, backAction):
        Menu.__init__(self, screen)
        self.config = config
        self.backAction = backAction
        self.loadingScreenGenerator = LoadingScreenGenerator(screen, config)
        self.createGameMenu = CreateGame(screen, self.initiateView, self.config, self.loadingScreenGenerator)

    def loadSavefile(self, savefileName: str) -> None:
        self.config.savefileName = savefileName

        if isfile(f"./savefiles/{savefileName}.json"):
            with open(f"./savefiles/{savefileName}.json") as savefile:
                saveData = json.load(savefile)
            game = Game(self.screen, self.config, saveData, self.loadingScreenGenerator)
            game.play()
        else:
            self.createGameMenu.initiateCreateGame()

    def deleteSavefile(self, savefileName: str):
        remove(f"./savefiles/{savefileName}.json")
        self.initiateView()

    def createDeleteSaveButton(self, buttonsList: list, savefileName: str, position: Vector2) -> None:
        if isfile(f"./savefiles/{savefileName}.json"):
            buttonsList.append(Button(pos=position,
                                      textInput="X",
                                      font=self.config.fontBig,
                                      action=self.deleteSavefile,
                                      actionArgument=savefileName,
                                      hoveringColor=DELETE_SAVEFILE_COLOR))
            
    def createSavefileButton(self, buttonsList: list, buttonText: str, savefileName: str, position: Vector2) -> Button:
        button = Button(pos=position,
                        textInput=buttonText,
                        font=self.config.fontBig,
                        action=self.loadSavefile,
                        actionArgument=savefileName)
        buttonsList.append(button)
        return button

    def createButtons(self) -> list[Button]:
        buttonsList = []

        savefile1Button = self.createSavefileButton(buttonsList, "SAVEFILE 1", "savefile1", Vector2(0.5 * self.config.WINDOW_WIDTH, 0.347 * self.config.WINDOW_HEIGHT))
        savefile2Button = self.createSavefileButton(buttonsList, "SAVEFILE 2", "savefile2", Vector2(0.5 * self.config.WINDOW_WIDTH, 0.486 * self.config.WINDOW_HEIGHT))
        savefile3Button = self.createSavefileButton(buttonsList, "SAVEFILE 3", "savefile3", Vector2(0.5 * self.config.WINDOW_WIDTH, 0.625 * self.config.WINDOW_HEIGHT))

        deleteButton1Position = Vector2(savefile1Button.rect.right + 100, 0.347 * self.config.WINDOW_HEIGHT)
        deleteButton2Position = Vector2(savefile1Button.rect.right + 100, 0.486 * self.config.WINDOW_HEIGHT)
        deleteButton3Position = Vector2(savefile1Button.rect.right + 100, 0.625 * self.config.WINDOW_HEIGHT)
        self.createDeleteSaveButton(buttonsList, "savefile1", deleteButton1Position)
        self.createDeleteSaveButton(buttonsList, "savefile2", deleteButton2Position)
        self.createDeleteSaveButton(buttonsList, "savefile3", deleteButton3Position)

        backButton = Button(pos=(0.5 * self.config.WINDOW_WIDTH, 0.764 * self.config.WINDOW_HEIGHT),
                            textInput="BACK",
                            font=self.config.fontBig,
                            action=self.backAction)
        buttonsList.append(backButton)
        return buttonsList


    def initiateView(self) -> None:
        self.createBackground()
        menuText = self.config.fontHuge.render("SELECT SAVEFILE", True, FONT_MENU_COLOR)
        menuRect = menuText.get_rect(center=(0.5 * self.config.WINDOW_WIDTH, 0.138 * self.config.WINDOW_HEIGHT))

        menuButtons = self.createButtons()
        menuTexts = [[menuText, menuRect]]

        self.menuLoop(menuTexts, menuButtons)
