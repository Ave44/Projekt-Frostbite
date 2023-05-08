from Config import Config
from constants import FONT_MENU_COLOR, BASE_BUTTON_COLOR
from menu.Menu import Menu
from menu.general.Button import Button


class CreateGame(Menu):
    def __init__(self, screen, backAction, config: Config):
        Menu.__init__(self, screen)
        self.backAction = backAction
        self.mapSizes = ["XS", "S", "M", "L", "XL"]
        self.mapSizesIndex = 2
        self.objectsQuantity = ["FEW", "NORMAL", "MANY"]
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
        if self.objectsQuantityIndex == 2:
            return
        self.objectsQuantityIndex += 1
        self.initiateCreateGame()

    def decrementObjectsQuantity(self) -> None:
        if self.objectsQuantityIndex == 0:
            return
        self.objectsQuantityIndex -= 1
        self.initiateCreateGame()

    def createGame(self) -> None:
        return

    def createButtons(self) -> list[Button]:
        mapSizeButtonIncrement = Button(pos=(0.95 * self.config.WINDOW_WIDTH, 0.347 * self.config.WINDOW_HEIGHT),
                                        textInput="=>",
                                        font=self.config.fontBig,
                                        action=self.incrementMapSize)

        mapSizeButtonDecrement = Button(pos=(0.05 * self.config.WINDOW_WIDTH, 0.347 * self.config.WINDOW_HEIGHT),
                                        textInput="<=",
                                        font=self.config.fontBig,
                                        action=self.decrementMapSize)

        objectsQuantityButtonIncrement = Button(pos=(0.95 * self.config.WINDOW_WIDTH, 0.486 * self.config.WINDOW_HEIGHT),
                                                textInput="=>",
                                                font=self.config.fontBig,
                                                action=self.incrementObjectsQuantity)

        objectsQuantityButtonDecrement = Button(pos=(0.05 * self.config.WINDOW_WIDTH, 0.486 * self.config.WINDOW_HEIGHT),
                                                textInput="<=",
                                                font=self.config.fontBig,
                                                action=self.decrementObjectsQuantity)

        createGameButton = Button(pos=(0.5 * self.config.WINDOW_WIDTH, 0.79 * self.config.WINDOW_HEIGHT),
                                  textInput="CREATE GAME",
                                  font=self.config.fontBig,
                                  action=self.createGame)

        backButton = Button(pos=(0.5 * self.config.WINDOW_WIDTH, 0.9 * self.config.WINDOW_HEIGHT),
                            textInput="BACK",
                            font=self.config.fontBig,
                            action=self.backAction)
        return [backButton, createGameButton, mapSizeButtonDecrement, mapSizeButtonIncrement,
                mapSizeButtonDecrement, objectsQuantityButtonIncrement, objectsQuantityButtonDecrement]

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
