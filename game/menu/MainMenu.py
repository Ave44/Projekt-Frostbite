from config import FONT_MENU_COLOR
from game.menu.CreateGame import CreateGame
from game.menu.Menu import Menu
from game.menu.OptionsMenu import OptionsMenu
from game.ui.general.Button import Button


class MainMenu(Menu):
    def __init__(self, screen, playAction):
        super().__init__(screen)
        self.play = playAction
        self.optionsMenu = OptionsMenu(screen, self.mainMenu)
        self.createGameMenu = CreateGame(screen, self.mainMenu)

    def mainMenu(self) -> None:
        self.createBackground()
        menuText = self.font.render("MAIN MENU", True, FONT_MENU_COLOR)
        menuRect = menuText.get_rect(center=(640, 100))
        play_button = Button(pos=(640, 250),
                             textInput="PLAY",
                             font=self.menuOptionFont,
                             action=self.play)
        create_game_button = Button(pos=(640, 350),
                                    textInput="CREATE GAME",
                                    font=self.menuOptionFont,
                                    action=self.createGameMenu.options)
        options_button = Button(pos=(640, 450),
                                textInput="OPTIONS",
                                font=self.menuOptionFont,
                                action=self.optionsMenu.options)
        quit_button = Button(pos=(640, 550),
                             textInput="QUIT",
                             font=self.menuOptionFont,
                             action=self.quitGame)
        menuButtons = [play_button, options_button, quit_button, create_game_button]

        self.menuLoop([[menuText, menuRect]], menuButtons)
