from config import FONT_MENU_COLOR, BASE_BUTTON_COLOR
from game.menu.Menu import Menu
from game.ui.general.Button import Button


class CreateGame(Menu):
    def __init__(self, screen, backAction):
        super().__init__(screen)
        self.backAction = backAction
        self.mapSizes = ["XS", "S", "M", "L", "XL"]
        self.mapSizesIndex = 2
        self.objectsQuantity = ["1", "2", "3", "4", "5"]
        self.objectsQuantityIndex = 2

    def increment_map_size(self) -> None:
        if self.mapSizesIndex == 4:
            return
        self.mapSizesIndex += 1
        self.options()

    def decrement_map_size(self) -> None:
        if self.mapSizesIndex == 0:
            return
        self.mapSizesIndex -= 1
        self.options()

    def incrementObjectsQuantity(self) -> None:
        if self.objectsQuantityIndex == 4:
            return
        self.objectsQuantityIndex += 1
        self.options()

    def decrementObjectsQuantity(self) -> None:
        if self.objectsQuantityIndex == 0:
            return
        self.objectsQuantityIndex -= 1
        self.options()

    def createGame(self) -> None:
        return

    def options(self) -> None:
        self.createBackground()
        menuText = self.font.render("CREATE GAME", True, FONT_MENU_COLOR)
        menuRect = menuText.get_rect(center=(640, 100))
        mapSizeText = self.menuOptionFont.render("MAP SIZE: " + self.mapSizes[self.mapSizesIndex], True,
                                                 BASE_BUTTON_COLOR)
        mapSizeRect = menuText.get_rect(center=(920, 275))
        objectsQuantityText = self.menuOptionFont.render(
            "OBJECTS QUANTITY: " + self.objectsQuantity[self.objectsQuantityIndex], True, BASE_BUTTON_COLOR)
        objectsQuantityRect = menuText.get_rect(center=(720, 375))

        map_size_button_increment = Button(pos=(1040, 250),
                                           textInput="=>",
                                           font=self.menuOptionFont,
                                           action=self.increment_map_size)
        map_size_button_decrement = Button(pos=(240, 250),
                                           textInput="<=",
                                           font=self.menuOptionFont,
                                           action=self.decrement_map_size)

        objects_quantity_button_increment = Button(pos=(1200, 350),
                                                   textInput="=>",
                                                   font=self.menuOptionFont,
                                                   action=self.incrementObjectsQuantity)
        objects_quantity_button_decrement = Button(pos=(80, 350),
                                                   textInput="<=",
                                                   font=self.menuOptionFont,
                                                   action=self.decrementObjectsQuantity)

        create_game_button = Button(pos=(640, 450),
                                    textInput="CREATE GAME",
                                    font=self.menuOptionFont,
                                    action=self.createGame)

        back_button = Button(pos=(640, 650),
                             textInput="BACK",
                             font=self.menuOptionFont,
                             action=self.backAction)
        menuButtons = [back_button, create_game_button, map_size_button_decrement, map_size_button_increment,
                       map_size_button_decrement, objects_quantity_button_increment, objects_quantity_button_decrement]
        menuTexts = [[menuText, menuRect], [mapSizeText, mapSizeRect], [objectsQuantityText, objectsQuantityRect]]

        self.menuLoop(menuTexts, menuButtons)
