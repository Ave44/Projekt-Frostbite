import json
from os import remove
from os.path import isfile
from pygame import Vector2

from constants import FONT_MENU_COLOR, DELETE_SAVEFILE_COLOR
from Config import Config
from game.Game import Game
from menu.Menu import Menu
from menu.general.Button import Button
from menu.general.Text import Text


class SaveSelectMenu(Menu):
    def __init__(self, config: Config, goToMainMenu: callable, goToCreateGameMenu: callable, refreshMenu: callable):
        Menu.__init__(self)
        self.config = config
        self.goToMainMenu = goToMainMenu
        self.goToCreateGameMenu = goToCreateGameMenu
        self.refreshMenu = refreshMenu
        self.createButtons()
        self.createTexts()

    def loadSavefile(self, savefileName: str) -> None:
        self.config.savefileName = savefileName

        if isfile(f"./savefiles/{savefileName}.json"):
            with open(f"./savefiles/{savefileName}.json") as savefile:
                saveData = json.load(savefile)
            game = Game(self.config, saveData)
            game.play()
        else:
            self.goToCreateGameMenu()

    def deleteSavefile(self, savefileName: str):
        remove(f"./savefiles/{savefileName}.json")
        self.refreshMenu()

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

    def createButtons(self) -> None:
        buttonsList = []

        savefile1Button = self.createSavefileButton(buttonsList, "SAVEFILE 1", "savefile1", Vector2(0.5 * self.config.WINDOW_WIDTH, 0.347 * self.config.WINDOW_HEIGHT))
        savefile2Button = self.createSavefileButton(buttonsList, "SAVEFILE 2", "savefile2", Vector2(0.5 * self.config.WINDOW_WIDTH, 0.486 * self.config.WINDOW_HEIGHT))
        savefile3Button = self.createSavefileButton(buttonsList, "SAVEFILE 3", "savefile3", Vector2(0.5 * self.config.WINDOW_WIDTH, 0.625 * self.config.WINDOW_HEIGHT))

        deleteButton1Position = Vector2(savefile1Button.rect.right + 100, 0.347 * self.config.WINDOW_HEIGHT)
        deleteButton2Position = Vector2(savefile2Button.rect.right + 100, 0.486 * self.config.WINDOW_HEIGHT)
        deleteButton3Position = Vector2(savefile3Button.rect.right + 100, 0.625 * self.config.WINDOW_HEIGHT)
        self.createDeleteSaveButton(buttonsList, "savefile1", deleteButton1Position)
        self.createDeleteSaveButton(buttonsList, "savefile2", deleteButton2Position)
        self.createDeleteSaveButton(buttonsList, "savefile3", deleteButton3Position)

        backButton = Button(pos=(0.5 * self.config.WINDOW_WIDTH, 0.764 * self.config.WINDOW_HEIGHT),
                            textInput="BACK",
                            font=self.config.fontBig,
                            action=self.goToMainMenu)
        buttonsList.append(backButton)
        
        self.buttons = buttonsList
    
    def createTexts(self) -> None:
        mainMenuTextPos = (0.5 * self.config.WINDOW_WIDTH, 0.138 * self.config.WINDOW_HEIGHT)
        mainMenuText = Text(mainMenuTextPos, "SELECT SAVEFILE", self.config.fontHuge, FONT_MENU_COLOR)

        self.texts = [mainMenuText]
