from config import FONT_MENU_COLOR
from menu.CreateGame import CreateGame
from menu.Menu import Menu
from menu.OptionsMenu import OptionsMenu
from game.ui.general.Button import Button


class MainMenu(Menu):
    def __init__(self, screen, playAction):
        super().__init__(screen)
        self.play = playAction
        self.optionsMenu = OptionsMenu(screen, self.mainMenu)
        self.createGameMenu = CreateGame(screen, self.mainMenu)

    def createButtons(self) -> list[Button]:
        playButton = Button(pos=(640, 250),
                            textInput="PLAY",
                            font=self.menuOptionFont,
                            action=self.play)
        createGameButton = Button(pos=(640, 350),
                                  textInput="CREATE GAME",
                                  font=self.menuOptionFont,
                                  action=self.createGameMenu.initiateCreateGame)
        optionsButton = Button(pos=(640, 450),
                               textInput="OPTIONS",
                               font=self.menuOptionFont,
                               action=self.optionsMenu.options)
        quitButton = Button(pos=(640, 550),
                            textInput="QUIT",
                            font=self.menuOptionFont,
                            action=self.quitGame)
        return [playButton, optionsButton, quitButton, createGameButton]

    def mainMenu(self) -> None:
        self.createBackground()
        menuText = self.font.render("MAIN MENU", True, FONT_MENU_COLOR)
        menuRect = menuText.get_rect(center=(640, 100))
        menuButtons = self.createButtons()

        self.menuLoop([[menuText, menuRect]], menuButtons)
