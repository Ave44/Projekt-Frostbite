import pygame
from pygame import mixer

from Config import Config
from constants import FONT_MENU_COLOR, BASE_BUTTON_COLOR
from menu.Menu import Menu
from menu.general.Button import Button


class OptionsMenu(Menu):
    def __init__(self, screen, backAction, config: Config):
        Menu.__init__(self, screen)
        self.backAction = backAction
        self.config = config
        if self.config.WINDOW_WIDTH == 1280:
            self.resolutionsIndex = 0
        else:
            self.resolutionsIndex = 1
        self.resolutions = ["1280x720", "1920x1080"]
        self.volume = ["0", "1", "2", "3", "4"]
        self.volumeIndex = 0

    def incrementResolution(self) -> None:
        if self.resolutionsIndex == 1:
            return
        else:
            self.resolutionsIndex += 1
            self.updateResolution()
            self.options()

    def decrementResolution(self) -> None:
        if self.resolutionsIndex == 0:
            return
        else:
            self.resolutionsIndex -= 1
            self.updateResolution()
            self.options()

    def incrementVolume(self) -> None:
        if self.volumeIndex == 4:
            return
        else:
            self.volumeIndex += 1
            self.updateMusicVolume()
            self.options()

    def decrementVolume(self) -> None:
        if self.volumeIndex == 0:
            return
        else:
            self.volumeIndex -= 1
            self.updateMusicVolume()
            self.options()

    def createButtons(self) -> list[Button]:
        backButton = Button(pos=(0.5 * self.config.WINDOW_WIDTH, 0.9 * self.config.WINDOW_HEIGHT),
                            textInput="BACK",
                            font=self.menuOptionFont,
                            action=self.backAction)

        resolutionButtonIncrement = Button(pos=(0.938 * self.config.WINDOW_WIDTH, 0.347 * self.config.WINDOW_HEIGHT),
                                           textInput="=>",
                                           font=self.menuOptionFont,
                                           action=self.incrementResolution)

        resolutionButtonDecrement = Button(pos=(0.063 * self.config.WINDOW_WIDTH, 0.347 * self.config.WINDOW_HEIGHT),
                                           textInput="<=",
                                           font=self.menuOptionFont,
                                           action=self.decrementResolution)

        volumeButtonIncrement = Button(pos=(0.938 * self.config.WINDOW_WIDTH, 0.486 * self.config.WINDOW_HEIGHT),
                                       textInput="=>",
                                       font=self.menuOptionFont,
                                       action=self.incrementVolume)

        volumeButtonDecrement = Button(pos=(0.063 * self.config.WINDOW_WIDTH, 0.486 * self.config.WINDOW_HEIGHT),
                                       textInput="<=",
                                       font=self.menuOptionFont,
                                       action=self.decrementVolume)

        return [backButton, resolutionButtonIncrement, resolutionButtonDecrement, volumeButtonIncrement,
                volumeButtonDecrement]

    def options(self) -> None:
        self.createBackground()
        menuText = self.font.render("OPTIONS", True, FONT_MENU_COLOR)
        menuRect = menuText.get_rect(center=(0.5 * self.config.WINDOW_WIDTH, 0.138 * self.config.WINDOW_HEIGHT))

        volumeText = self.menuOptionFont.render("VOLUME: " + self.volume[self.volumeIndex], True,
                                                BASE_BUTTON_COLOR)
        volumeRect = menuText.get_rect(center=(0.563 * self.config.WINDOW_WIDTH, 0.52 * self.config.WINDOW_HEIGHT))

        resolutionText = self.menuOptionFont.render(
            "HUD: " + self.resolutions[self.resolutionsIndex], True, BASE_BUTTON_COLOR)
        resolutionRect = menuText.get_rect(center=(0.5 * self.config.WINDOW_WIDTH, 0.37 * self.config.WINDOW_HEIGHT))

        menuButtons = self.createButtons()

        self.menuLoop([[menuText, menuRect], [volumeText, volumeRect], [resolutionText, resolutionRect]], menuButtons)

    def updateResolution(self):
        if self.resolutions[self.resolutionsIndex] == "1920x1080":
            self.config.WINDOW_HEIGHT = 1080
            self.config.WINDOW_WIDTH = 1920
            self.updateScreen()
        else:
            self.config.WINDOW_HEIGHT = 720
            self.config.WINDOW_WIDTH = 1080
            self.updateScreen()

    def updateScreen(self):
        screen = pygame.display.set_mode((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT))
        resized_screen = pygame.transform.scale(screen, (self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT))
        self.screen.blit(resized_screen, (0, 0))

    def updateMusicVolume(self):
        self.config.MUSIC_VOLUME = int(self.volume[self.volumeIndex]) * 0.2
        mixer.music.set_volume(self.config.MUSIC_VOLUME)
