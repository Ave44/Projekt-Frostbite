import pygame
from pygame import mixer, Surface

from Config import Config
from constants import FONT_MENU_COLOR, BASE_BUTTON_COLOR, PIXEL_FONT, NORMAL_FONT
from menu.Menu import Menu
from menu.general.Button import Button
from pygame._sdl2.video import Window


class OptionsMenu(Menu):
    def __init__(self, screen: Surface, backAction, config: Config):
        Menu.__init__(self, screen)
        self.backAction = backAction
        self.config = config
        if self.config.WINDOW_WIDTH == 1280:
            self.resolutionsIndex = 0
        else:
            self.resolutionsIndex = 1
        self.resolutions = ["1280x720", "1920x1080", "Fullscreen"]
        self.volume = ["0", "1", "2", "3", "4"]
        self.fonts = ["Pixel", "Normal"]
        self.volumeIndex = 0
        self.fontIndex = 0

    def incrementResolution(self) -> None:
        if self.resolutionsIndex == 2:
            return
        else:
            self.resolutionsIndex += 1
            self.updateResolution()
            self.refreshMenu()

    def decrementResolution(self) -> None:
        if self.resolutionsIndex == 0:
            return
        else:
            self.resolutionsIndex -= 1
            self.updateResolution()
            self.refreshMenu()

    def incrementFont(self) -> None:
        if self.fontIndex == 1:
            return
        else:
            self.fontIndex += 1
            self.updateFont()
            self.refreshMenu()

    def decrementFont(self) -> None:
        if self.fontIndex == 0:
            return
        else:
            self.fontIndex -= 1
            self.updateFont()
            self.refreshMenu()

    def incrementVolume(self) -> None:
        if self.volumeIndex == 4:
            return
        else:
            self.volumeIndex += 1
            self.updateMusicVolume()
            self.refreshMenu()

    def decrementVolume(self) -> None:
        if self.volumeIndex == 0:
            return
        else:
            self.volumeIndex -= 1
            self.updateMusicVolume()
            self.refreshMenu()

    def createButtons(self) -> list[Button]:
        backButton = Button(pos=(0.5 * self.config.WINDOW_WIDTH, 0.9 * self.config.WINDOW_HEIGHT),
                            textInput="BACK",
                            font=self.config.fontBig,
                            action=self.backAction)

        resolutionButtonIncrement = Button(pos=(0.95 * self.config.WINDOW_WIDTH, 0.347 * self.config.WINDOW_HEIGHT),
                                           textInput="=>",
                                           font=self.config.fontBig,
                                           action=self.incrementResolution)

        resolutionButtonDecrement = Button(pos=(0.05 * self.config.WINDOW_WIDTH, 0.347 * self.config.WINDOW_HEIGHT),
                                           textInput="<=",
                                           font=self.config.fontBig,
                                           action=self.decrementResolution)

        volumeButtonIncrement = Button(pos=(0.95 * self.config.WINDOW_WIDTH, 0.486 * self.config.WINDOW_HEIGHT),
                                       textInput="=>",
                                       font=self.config.fontBig,
                                       action=self.incrementVolume)

        volumeButtonDecrement = Button(pos=(0.05 * self.config.WINDOW_WIDTH, 0.486 * self.config.WINDOW_HEIGHT),
                                       textInput="<=",
                                       font=self.config.fontBig,
                                       action=self.decrementVolume)

        fontButtonIncrement = Button(pos=(0.95 * self.config.WINDOW_WIDTH, 0.627 * self.config.WINDOW_HEIGHT),
                                       textInput="=>",
                                       font=self.config.fontBig,
                                       action=self.incrementFont)

        fontButtonDecrement = Button(pos=(0.05 * self.config.WINDOW_WIDTH, 0.627 * self.config.WINDOW_HEIGHT),
                                       textInput="<=",
                                       font=self.config.fontBig,
                                       action=self.decrementFont)

        return [backButton, resolutionButtonIncrement, resolutionButtonDecrement, volumeButtonIncrement,
                volumeButtonDecrement, fontButtonDecrement, fontButtonIncrement]

    def refreshMenu(self) -> None:
        self.createBackground()
        menuText = self.config.fontHuge.render("OPTIONS", True, FONT_MENU_COLOR)
        menuRect = menuText.get_rect(center=(0.5 * self.config.WINDOW_WIDTH, 0.138 * self.config.WINDOW_HEIGHT))

        volumeText = self.config.fontBig.render("VOLUME: " + self.volume[self.volumeIndex], True,
                                                BASE_BUTTON_COLOR)
        volumeRect = menuText.get_rect(center=(0.5 * self.config.WINDOW_WIDTH, 0.52 * self.config.WINDOW_HEIGHT))

        resolutionText = self.config.fontBig.render(
            "HUD: " + self.resolutions[self.resolutionsIndex], True, BASE_BUTTON_COLOR)
        resolutionRect = menuText.get_rect(center=(0.5 * self.config.WINDOW_WIDTH, 0.37 * self.config.WINDOW_HEIGHT))

        fontText = self.config.fontBig.render(
            "FONT: " + self.fonts[self.fontIndex], True, BASE_BUTTON_COLOR)
        fontRect = menuText.get_rect(center=(0.5 * self.config.WINDOW_WIDTH, 0.65 * self.config.WINDOW_HEIGHT))

        menuButtons = self.createButtons()

        self.menuLoop([[menuText, menuRect], [volumeText, volumeRect], [resolutionText, resolutionRect], [fontText, fontRect]], menuButtons)

    def updateResolution(self) -> None:
        if self.resolutionsIndex == 2:
            infoObject = pygame.display.Info()
            self.config.WINDOW_HEIGHT = infoObject.current_h
            self.config.WINDOW_WIDTH = infoObject.current_w
            self.updateScreen()
        elif self.resolutionsIndex == 1:
            self.config.WINDOW_HEIGHT = 1080
            self.config.WINDOW_WIDTH = 1920
            self.updateScreen()
        else:
            self.config.WINDOW_HEIGHT = 720
            self.config.WINDOW_WIDTH = 1080
            self.updateScreen()

    def updateScreen(self) -> None:
        if self.resolutionsIndex == 0:
            self.screen = pygame.display.set_mode((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT))
            window = Window.from_display_module()
            window.position = (400, 200)
            return
        else:
            self.screen = pygame.display.set_mode((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT), pygame.FULLSCREEN)

    def updateMusicVolume(self) -> None:
        self.config.MUSIC_VOLUME = int(self.volume[self.volumeIndex]) * 0.2
        mixer.music.set_volume(self.config.MUSIC_VOLUME)

    def updateFont(self) -> None:
        if self.fontIndex == 1:
            self.config.setFont(NORMAL_FONT)
        else:
            self.config.setFont(PIXEL_FONT)
