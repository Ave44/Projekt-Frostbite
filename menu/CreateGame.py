from pygame import Vector2
from json import dump

from Config import Config
from constants import FONT_MENU_COLOR, BASE_BUTTON_COLOR
from menu.Menu import Menu
from menu.general.Button import Button
from menu.general.Text import Text
from gameInitialization.GenerateMap import generateMap
from game.Game import Game
from menu.general.LoadingScreenGenerator import LoadingScreenGenerator


class CreateGame(Menu):
    def __init__(self, config: Config, goToSaveSelectMenu: callable, refreshMenu: callable, returnToMainMenu: callable):
        Menu.__init__(self)
        self.goToSaveSelectMenu = goToSaveSelectMenu
        self.returnToMainMenu = returnToMainMenu
        self.refreshMenu = refreshMenu
        self.mapSizes = ["XS", "S", "M", "L", "XL"]
        self.mapSizesList = [50, 75, 100, 150, 200]
        self.mapSizesIndex = 2
        self.objectsQuantity = ["VERY FEW", "FEW", "NORMAL", "MANY", "LOTS"]
        self.objectsQuantityList = [0.25, 0.5, 1, 1.5, 2]
        self.objectsQuantityIndex = 2
        self.config = config
        self.createButtons()
        self.createTexts()

    def incrementMapSize(self) -> None:
        if self.mapSizesIndex < 4:
            self.mapSizesIndex += 1
            self.refreshMenu()

    def decrementMapSize(self) -> None:
        if self.mapSizesIndex > 0:
            self.mapSizesIndex -= 1
            self.refreshMenu()

    def incrementObjectsQuantity(self) -> None:
        if self.objectsQuantityIndex < 4:
            self.objectsQuantityIndex += 1
            self.refreshMenu()

    def decrementObjectsQuantity(self) -> None:
        if self.objectsQuantityIndex > 0:
            self.objectsQuantityIndex -= 1
            self.refreshMenu()

    def goBack(self):
        self.mapSizesIndex = 2
        self.objectsQuantityIndex = 2
        self.refreshMenu()
        self.goToSaveSelectMenu()

    def createGame(self) -> None:
        mapSize = self.mapSizesList[self.mapSizesIndex]
        objectsQuantity = self.objectsQuantityList[self.objectsQuantityIndex]
        loadingScreenGenerator = LoadingScreenGenerator(self.config)
        mapRaw, mapData, objects = generateMap(mapSize, objectsQuantity, loadingScreenGenerator.generateLoadingScreen)
        saveData = {'map': mapRaw, 'currentDay': 1, 'currentTimeMs': 50000, 'sprites': objects}
        with open(f"savefiles/{self.config.savefileName}.json", "w") as file:
            dump(saveData, file)
        game = Game(self.config, saveData, self.returnToMainMenu)
        game.play()

    def createButton(self, buttonsList: list, position: Vector2, buttonText: str, action: callable) -> Button:
        button = Button(pos=position,
                        textInput=buttonText,
                        font=self.config.fontBig,
                        action=action)
        buttonsList.append(button)
        return button

    def createButtons(self) -> None:
        buttonsList = []
        self.createButton(buttonsList, Vector2(0.5 * self.config.WINDOW_WIDTH, 0.9 * self.config.WINDOW_HEIGHT), "BACK", self.goBack)
        self.createButton(buttonsList, Vector2(0.5 * self.config.WINDOW_WIDTH, 0.79 * self.config.WINDOW_HEIGHT), "CREATE GAME", self.createGame)

        if self.mapSizesIndex < len(self.mapSizes) - 1:
            position = Vector2(0.95 * self.config.WINDOW_WIDTH, 0.347 * self.config.WINDOW_HEIGHT)
            self.createButton(buttonsList, position, "=>", self.incrementMapSize)

        if self.mapSizesIndex > 0:
            position = Vector2(0.05 * self.config.WINDOW_WIDTH, 0.347 * self.config.WINDOW_HEIGHT)
            self.createButton(buttonsList, position, "<=", self.decrementMapSize)

        if self.objectsQuantityIndex < len(self.objectsQuantity) - 1:
            position = Vector2(0.95 * self.config.WINDOW_WIDTH, 0.486 * self.config.WINDOW_HEIGHT)
            self.createButton(buttonsList, position, "=>", self.incrementObjectsQuantity)

        if self.objectsQuantityIndex > 0:
            position = Vector2(0.05 * self.config.WINDOW_WIDTH, 0.486 * self.config.WINDOW_HEIGHT)
            self.createButton(buttonsList, position, "<=", self.decrementObjectsQuantity)

        self.buttons = buttonsList
    
    def createTexts(self) -> None:
        mainMenuTextPos = (0.5 * self.config.WINDOW_WIDTH, 0.138 * self.config.WINDOW_HEIGHT)
        mainMenuText = Text(mainMenuTextPos, "CREATE GAME", self.config.fontHuge, FONT_MENU_COLOR)

        mapSizeTextPos = (0.5 * self.config.WINDOW_WIDTH, 0.37 * self.config.WINDOW_HEIGHT)
        mapSizeTextContent = "MAP SIZE: " + self.mapSizes[self.mapSizesIndex]
        mapSizeText = Text(mapSizeTextPos, mapSizeTextContent, self.config.fontBig, BASE_BUTTON_COLOR)

        objectsQuantityTextPos = (0.5 * self.config.WINDOW_WIDTH, 0.52 * self.config.WINDOW_HEIGHT)
        objectsQuantityTextContent = "OBJECTS: " + self.objectsQuantity[self.objectsQuantityIndex]
        objectsQuantityText = Text(objectsQuantityTextPos, objectsQuantityTextContent, self.config.fontBig, BASE_BUTTON_COLOR)

        self.texts = [mainMenuText, mapSizeText, objectsQuantityText]
