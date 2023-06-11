import pygame
from pygame import mixer, Vector2

from Config import Config
from constants import FONT_MENU_COLOR, BASE_BUTTON_COLOR, PIXEL_FONT, NORMAL_FONT
from menu.Menu import Menu
from menu.general.Button import Button
from menu.general.Text import Text


class OptionsMenu(Menu):
    def __init__(self, config: Config, goToMainMenu: callable, refreshMenu: callable, refreshAllMenus: callable):
        Menu.__init__(self)
        self.goToMainMenu = goToMainMenu
        self.refreshMenu = refreshMenu
        self.refreshAllMenus = refreshAllMenus
        self.config = config
        
        self.resolutionsIndex = 2
        self.resolutions = ["1280x720", "1920x1080", "Fullscreen"]

        self.volume = ["0", "0.25", "0.5", "0.75", "1"]
        self.volumeList = [0, 0.25, 0.5, 0.75, 1]
        self.volumeIndex = 2

        self.fontIndex = 0
        self.fonts = ["Pixel", "Normal"]

        self.createButtons()
        self.createTexts()

    def incrementResolution(self) -> None:
        if self.resolutionsIndex < 2:
            self.resolutionsIndex += 1
            self.updateResolution()

    def decrementResolution(self) -> None:
        if self.resolutionsIndex > 0:
            self.resolutionsIndex -= 1
            self.updateResolution()

    def incrementFont(self) -> None:
        if self.fontIndex < 1:
            self.fontIndex += 1
            self.updateFont()

    def decrementFont(self) -> None:
        if self.fontIndex > 0:
            self.fontIndex -= 1
            self.updateFont()

    def incrementVolume(self) -> None:
        if self.volumeIndex < 4:
            self.volumeIndex += 1
            self.updateMusicVolume()

    def decrementVolume(self) -> None:
        if self.volumeIndex > 0:
            self.volumeIndex -= 1
            self.updateMusicVolume()

    def createButton(self, buttonsList: list, position: Vector2, buttonText: str, action: callable) -> Button:
        button = Button(pos=position,
                        textInput=buttonText,
                        font=self.config.fontBig,
                        action=action)
        buttonsList.append(button)
        return button

    def createButtons(self) -> None:
        buttonsList = []
        self.createButton(buttonsList, Vector2(0.5 * self.config.WINDOW_WIDTH, 0.9 * self.config.WINDOW_HEIGHT), "BACK",
                          self.goToMainMenu)

        if self.resolutionsIndex < len(self.resolutions) - 1:
            position = Vector2(0.95 * self.config.WINDOW_WIDTH, 0.347 * self.config.WINDOW_HEIGHT)
            self.createButton(buttonsList, position, "=>", self.incrementResolution)

        if self.resolutionsIndex > 0:
            position = Vector2(0.05 * self.config.WINDOW_WIDTH, 0.347 * self.config.WINDOW_HEIGHT)
            self.createButton(buttonsList, position, "<=", self.decrementResolution)

        if self.volumeIndex < len(self.volume) - 1:
            position = Vector2(0.95 * self.config.WINDOW_WIDTH, 0.486 * self.config.WINDOW_HEIGHT)
            self.createButton(buttonsList, position, "=>", self.incrementVolume)

        if self.volumeIndex > 0:
            position = Vector2(0.05 * self.config.WINDOW_WIDTH, 0.486 * self.config.WINDOW_HEIGHT)
            self.createButton(buttonsList, position, "<=", self.decrementVolume)

        if self.fontIndex < len(self.fonts) - 1:
            position = Vector2(0.95 * self.config.WINDOW_WIDTH, 0.627 * self.config.WINDOW_HEIGHT)
            self.createButton(buttonsList, position, "=>", self.incrementFont)

        if self.fontIndex > 0:
            position = Vector2(0.05 * self.config.WINDOW_WIDTH, 0.627 * self.config.WINDOW_HEIGHT)
            self.createButton(buttonsList, position, "<=", self.decrementFont)

        self.buttons = buttonsList
    
    def createTexts(self) -> None:
        menuTextPos = (0.5 * self.config.WINDOW_WIDTH, 0.138 * self.config.WINDOW_HEIGHT)
        menuText = Text(menuTextPos, "OPTIONS", self.config.fontHuge, FONT_MENU_COLOR)

        volumeTextPos = (0.5 * self.config.WINDOW_WIDTH, 0.52 * self.config.WINDOW_HEIGHT)
        volumeTextContent = "VOLUME: " + self.volume[self.volumeIndex]
        volumeText = Text(volumeTextPos, volumeTextContent, self.config.fontBig, BASE_BUTTON_COLOR)

        resolutionTextPos = (0.5 * self.config.WINDOW_WIDTH, 0.37 * self.config.WINDOW_HEIGHT)
        resolutionTextContent = "HUD: " + self.resolutions[self.resolutionsIndex]
        resolutionText = Text(resolutionTextPos, resolutionTextContent, self.config.fontBig, BASE_BUTTON_COLOR)

        fontTextPos = (0.5 * self.config.WINDOW_WIDTH, 0.65 * self.config.WINDOW_HEIGHT)
        fontTextContent = "FONT: " + self.fonts[self.fontIndex]
        fontText = Text(fontTextPos, fontTextContent, self.config.fontBig, BASE_BUTTON_COLOR)

        self.texts = [menuText, volumeText, resolutionText, fontText]

    def updateResolution(self) -> None:
        if self.resolutionsIndex == 2:
            self.config.setWindowSize(self.config.monitorWidth, self.config.monitorHeight)
            pygame.display.set_mode((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT), pygame.FULLSCREEN)
        elif self.resolutionsIndex == 1:
            self.config.setWindowSize(1920, 1080)
            pygame.display.set_mode((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT))
            positonX = 20 if self.config.monitorWidth > 1920 else 0
            positonY = 20 if self.config.monitorHeight > 1080 else 0
            self.config.window.position = (positonX, positonY)
        else:
            self.config.setWindowSize(1080, 720)
            pygame.display.set_mode((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT))
            self.config.window.position = (400, 200)

        self.createBackground()
        self.refreshAllMenus()

    def updateMusicVolume(self) -> None:
        self.config.MUSIC_VOLUME = self.volumeList[self.volumeIndex]
        mixer.music.set_volume(self.config.MUSIC_VOLUME)
        self.refreshMenu()

    def updateFont(self) -> None:
        if self.fontIndex == 1:
            self.config.setFont(NORMAL_FONT)
        else:
            self.config.setFont(PIXEL_FONT)
        self.refreshAllMenus()
