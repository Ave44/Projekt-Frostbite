from config import FONT_MENU_COLOR, BASE_BUTTON_COLOR
from menu.Menu import Menu
from menu.general.Button import Button


class CreateGame(Menu):
    def __init__(self, screen, backAction):
        super().__init__(screen)
        self.backAction = backAction
        self.mapSizes = ["XS", "S", "M", "L", "XL"]
        self.mapSizesIndex = 2
        self.objectsQuantity = ["1", "2", "3", "4", "5"]
        self.objectsQuantityIndex = 2

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
        return

    def createButtons(self) -> list[Button]:
        mapSizeButtonIncrement = Button(pos=(1200, 250),
                                        textInput="=>",
                                        font=self.menuOptionFont,
                                        action=self.incrementMapSize)

        mapSizeButtonDecrement = Button(pos=(80, 250),
                                        textInput="<=",
                                        font=self.menuOptionFont,
                                        action=self.decrementMapSize)

        objectsQuantityButtonIncrement = Button(pos=(1200, 350),
                                                textInput="=>",
                                                font=self.menuOptionFont,
                                                action=self.incrementObjectsQuantity)

        objectsQuantityButtonDecrement = Button(pos=(80, 350),
                                                textInput="<=",
                                                font=self.menuOptionFont,
                                                action=self.decrementObjectsQuantity)

        createGameButton = Button(pos=(640, 450),
                                  textInput="CREATE GAME",
                                  font=self.menuOptionFont,
                                  action=self.createGame)

        backButton = Button(pos=(640, 650),
                            textInput="BACK",
                            font=self.menuOptionFont,
                            action=self.backAction)
        return [backButton, createGameButton, mapSizeButtonDecrement, mapSizeButtonIncrement,
                mapSizeButtonDecrement, objectsQuantityButtonIncrement, objectsQuantityButtonDecrement]

    def initiateCreateGame(self) -> None:
        self.createBackground()
        menuText = self.font.render("CREATE GAME", True, FONT_MENU_COLOR)
        menuRect = menuText.get_rect(center=(640, 100))
        mapSizeText = self.menuOptionFont.render("MAP SIZE: " + self.mapSizes[self.mapSizesIndex], True,
                                                 BASE_BUTTON_COLOR)
        mapSizeRect = menuText.get_rect(center=(920, 275))
        objectsQuantityText = self.menuOptionFont.render(
            "OBJECTS QUANTITY: " + self.objectsQuantity[self.objectsQuantityIndex], True, BASE_BUTTON_COLOR)
        objectsQuantityRect = menuText.get_rect(center=(720, 375))

        menuButtons = self.createButtons()
        menuTexts = [[menuText, menuRect], [mapSizeText, mapSizeRect], [objectsQuantityText, objectsQuantityRect]]

        self.menuLoop(menuTexts, menuButtons)
