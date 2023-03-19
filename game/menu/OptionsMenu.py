from config import FONT_MENU_COLOR, BASE_BUTTON_COLOR, WHITE
from game.menu.Menu import Menu
from game.ui.general.Button import Button


class OptionsMenu(Menu):
    def __init__(self, screen, backAction):
        super().__init__(screen)
        self.backAction = backAction

    def options(self) -> None:
        self.createBackground()
        menuText = self.font.render("OPTIONS", True, FONT_MENU_COLOR)
        menuRect = menuText.get_rect(center=(640, 100))
        back_button = Button(pos=(640, 650),
                             textInput="BACK",
                             font=self.menuOptionFont, baseColor=BASE_BUTTON_COLOR, hoveringColor=WHITE,
                             action=self.backAction)
        menuButtons = [back_button]

        self.menuLoop([[menuText, menuRect]], menuButtons)
