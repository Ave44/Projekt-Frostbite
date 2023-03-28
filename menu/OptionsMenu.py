from config import FONT_MENU_COLOR, BASE_BUTTON_COLOR
from menu.Menu import Menu
from menu.general.Button import Button


class OptionsMenu(Menu):
    def __init__(self, screen, backAction):
        super().__init__(screen)
        self.backAction = backAction
        self.resolutions = ["1280x720", "1920x1080"]
        self.resolutionsIndex = 0
        self.volume = ["0", "1", "2", "3", "4"]
        self.volumeIndex = 0

    def incrementResolution(self) -> None:
        if self.resolutionsIndex == 1:
            return
        self.resolutionsIndex += 1
        self.options()

    def decrementResolution(self) -> None:
        if self.resolutionsIndex == 0:
            return
        self.resolutionsIndex -= 1
        self.options()

    def incrementVolume(self) -> None:
        if self.volumeIndex == 4:
            return
        self.volumeIndex += 1
        self.options()

    def decrementVolume(self) -> None:
        if self.volumeIndex == 0:
            return
        self.volumeIndex -= 1
        self.options()

    def createButtons(self) -> list[Button]:
        backButton = Button(pos=(640, 650),
                            textInput="BACK",
                            font=self.menuOptionFont,
                            action=self.backAction)

        resolutionButtonIncrement = Button(pos=(1200, 250),
                                           textInput="=>",
                                           font=self.menuOptionFont,
                                           action=self.incrementResolution)

        resolutionButtonDecrement = Button(pos=(80, 250),
                                           textInput="<=",
                                           font=self.menuOptionFont,
                                           action=self.decrementResolution)

        volumeButtonIncrement = Button(pos=(1200, 350),
                                       textInput="=>",
                                       font=self.menuOptionFont,
                                       action=self.incrementVolume)

        volumeButtonDecrement = Button(pos=(80, 350),
                                       textInput="<=",
                                       font=self.menuOptionFont,
                                       action=self.decrementVolume)

        return [backButton, resolutionButtonIncrement, resolutionButtonDecrement, volumeButtonIncrement,
                volumeButtonDecrement]

    def options(self) -> None:
        self.createBackground()
        menuText = self.font.render("OPTIONS", True, FONT_MENU_COLOR)
        menuRect = menuText.get_rect(center=(640, 100))

        volumeText = self.menuOptionFont.render("VOLUME: " + self.volume[self.volumeIndex], True,
                                                BASE_BUTTON_COLOR)
        volumeRect = menuText.get_rect(center=(720, 375))

        resolutionText = self.menuOptionFont.render(
            "HUD: " + self.resolutions[self.resolutionsIndex], True, BASE_BUTTON_COLOR)
        resolutionRect = menuText.get_rect(center=(660, 275))

        menuButtons = self.createButtons()

        self.menuLoop([[menuText, menuRect], [volumeText, volumeRect], [resolutionText, resolutionRect]], menuButtons)
