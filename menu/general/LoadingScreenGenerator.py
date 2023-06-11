from pygame import display

from Config import Config
from constants import FONT_MENU_COLOR


class LoadingScreenGenerator:
    def __init__(self, config: Config):
        self.screen = display.get_surface()
        self.config = config

    def generateLoadingScreen(self, information: str) -> None:
        self.screen.fill((0, 0, 0))
        infoText = self.config.fontBig.render(information, True, FONT_MENU_COLOR)
        infoRect = infoText.get_rect(center=(0.5 * self.config.WINDOW_WIDTH, 0.5 * self.config.WINDOW_HEIGHT))
        self.screen.blit(infoText, infoRect)
        display.flip()
