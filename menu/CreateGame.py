from pygame import display, Vector2
from json import dump

from Config import Config
from constants import FONT_MENU_COLOR, BASE_BUTTON_COLOR
from menu.Menu import Menu
from menu.general.Button import Button
from gameInitialization.GenerateMap import generateMap
from game.Game import Game


class CreateGame(Menu):
    def __init__(self, screen, backAction, config: Config):
        Menu.__init__(self, screen)
        self.backAction = backAction
        self.mapSizes = ["XS", "S", "M", "L", "XL"]
        self.mapSizesList = [50, 75, 100, 150, 200]
        self.mapSizesIndex = 2
        self.objectsQuantity = ["VERY FEW", "FEW", "NORMAL", "MANY", "LOTS"]
        self.objectsQuantityList = [0.25, 0.5, 1, 1.5, 2]
        self.objectsQuantityIndex = 2
        self.config = config

    def incrementMapSize(self) -> None:
        if self.mapSizesIndex == 4:
            return
        self.mapSizesIndex += 1
        self.initiateCreateGame()

    def decrementMapSize(self) -> None:
        if self.mapSizesIndex == 0:
            return
        self.mapSizesIndex -= 1
        self.initiateCreateGame()

    def incrementObjectsQuantity(self) -> None:
        if self.objectsQuantityIndex == 4:
            return
        self.objectsQuantityIndex += 1
        self.initiateCreateGame()

    def decrementObjectsQuantity(self) -> None:
        if self.objectsQuantityIndex == 0:
            return
        self.objectsQuantityIndex -= 1
        self.initiateCreateGame()

    def createGame(self) -> None:
        mapSize = self.mapSizesList[self.mapSizesIndex]
        objectsQuantity = self.objectsQuantityList[self.objectsQuantityIndex]
        mapRaw, mapData, objects = generateMap(mapSize, objectsQuantity, self.generateMapLoadingScreen)
        saveData = {'map': mapRaw, 'currentDay': 1, 'currentTimeMs': 60000, 'sprites': objects}
        with open(f"savefiles/{self.config.savefileName}.json", "w") as file:
            dump(saveData, file)
        game = Game(self.screen, self.config, saveData)
        game.play()

    def generateMapLoadingScreen(self, information: str) -> None:
        self.screen.fill((0, 0, 0))
        infoText = self.config.fontBig.render(information, True, FONT_MENU_COLOR)
        infoRect = infoText.get_rect(center=(0.5 * self.config.WINDOW_WIDTH, 0.5 * self.config.WINDOW_HEIGHT))
        self.screen.blit(infoText, infoRect)
        display.flip()

    def createButton(self, buttonsList: list, position: Vector2, buttonText: str, action: callable) -> Button:
        button = Button(pos=position,
                        textInput=buttonText,
                        font=self.config.fontBig,
                        action=action)
        buttonsList.append(button)
        return button

    def createButtons(self) -> list[Button]:
        buttonsList = []
        self.createButton(buttonsList, Vector2(0.5 * self.config.WINDOW_WIDTH, 0.9 * self.config.WINDOW_HEIGHT), "BACK", self.backAction)
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

        return buttonsList

    def initiateCreateGame(self) -> None:
        self.createBackground()
        menuText = self.config.fontHuge.render("CREATE GAME", True, FONT_MENU_COLOR)
        menuRect = menuText.get_rect(center=(0.5 * self.config.WINDOW_WIDTH, 0.138 * self.config.WINDOW_HEIGHT))
        mapSizeText = self.config.fontBig.render("MAP SIZE: " + self.mapSizes[self.mapSizesIndex], True,
                                                 BASE_BUTTON_COLOR)
        mapSizeRect = menuText.get_rect(center=(0.6 * self.config.WINDOW_WIDTH, 0.37 * self.config.WINDOW_HEIGHT))
        objectsQuantityText = self.config.fontBig.render(
            "OBJECTS: " + self.objectsQuantity[self.objectsQuantityIndex], True, BASE_BUTTON_COLOR)
        objectsQuantityRect = menuText.get_rect(center=(0.6 * self.config.WINDOW_WIDTH, 0.52 * self.config.WINDOW_HEIGHT))

        menuButtons = self.createButtons()
        menuTexts = [[menuText, menuRect], [mapSizeText, mapSizeRect], [objectsQuantityText, objectsQuantityRect]]

        self.menuLoop(menuTexts, menuButtons)
