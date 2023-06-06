import sys

import pygame
from pygame import mixer, MOUSEMOTION, MOUSEBUTTONDOWN, QUIT
from pygame.event import Event

from Config import Config
from constants import MENU_THEME

from menu.Menu import Menu
from menu.MainMenu import MainMenu
from menu.OptionsMenu import OptionsMenu
from menu.CreateGame import CreateGame
from menu.SaveSelectMenu import SaveSelectMenu

class MenuController:
    def __init__(self, config: Config):
        self.screen = pygame.display.get_surface()
        self.mainMenu = MainMenu(config, self.goToSaveSelectMenu, self.goToOptionsMenu)
        self.optionsMenu = OptionsMenu(config, self.goToMainMenu, self.refreshMenu, self.refreshAllMenus)
        self.createGame = CreateGame(config, self.goToSaveSelectMenu, self.refreshMenu)
        self.saveSelectMenu = SaveSelectMenu(config, self.goToMainMenu, self.goToCreateGameMenu, self.refreshMenu)

        self.currentMenu = self.mainMenu
        mixer.music.load(MENU_THEME)
        mixer.music.play(-1)

    def goToMainMenu(self) -> None:
        self.changeCurrentMenu(self.mainMenu)

    def goToOptionsMenu(self) -> None:
        self.changeCurrentMenu(self.optionsMenu)

    def goToCreateGameMenu(self) -> None:
        self.changeCurrentMenu(self.createGame)

    def goToSaveSelectMenu(self) -> None:
        self.changeCurrentMenu(self.saveSelectMenu)

    def changeCurrentMenu(self, menu: Menu) -> None:
        self.currentMenu = menu
        self.drawMenu()

    def returnToMainMenu(self) -> None:
        mixer.music.load(MENU_THEME)
        mixer.music.play(-1)
        self.mainMenu()

    def handleEvent(self, event: Event) -> None:
        if event.type == MOUSEMOTION:
            self.drawMenu()
            
        if event.type == MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            for button in self.currentMenu.buttons:
                if button.checkForInput(mousePos):
                    button.executeAction()

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    def drawMenu(self) -> None:
        self.updateButtons()
        self.screen.blit(self.currentMenu.background, (0, 0))

        for text in self.currentMenu.texts:
            text.draw(self.screen)

        for button in self.currentMenu.buttons:
            button.draw(self.screen)

        pygame.display.update()

    def updateButtons(self) -> None:
        mousePos = pygame.mouse.get_pos()
        for button in self.currentMenu.buttons:
            button.update(mousePos)

    def refreshAllMenus(self) -> None:
        self.mainMenu.reinitializeMenu()
        self.optionsMenu.reinitializeMenu()
        self.createGame.reinitializeMenu()
        self.saveSelectMenu.reinitializeMenu()
        self.drawMenu()

    def refreshMenu(self) -> None:
        self.currentMenu.reinitializeMenu()
        self.drawMenu()

    def menuLoop(self) -> None:
        self.drawMenu()
        while True:
            event = pygame.event.wait()
            self.handleEvent(event)
