from math import ceil

from pygame.font import Font

from constants import TILE_SIZE, PIXEL_FONT


class Config:
    def __init__(self) -> None:
        self.WINDOW_WIDTH = 1920
        self.WINDOW_HEIGHT = 1080
        self.TILES_ON_SCREEN_WIDTH = ceil(self.WINDOW_WIDTH / TILE_SIZE + 1)
        self.TILES_ON_SCREEN_HEIGHT = ceil(self.WINDOW_HEIGHT / TILE_SIZE + 1)

        # MUSIC
        self.MUSIC_VOLUME = 0
        self.SOUNDS_VOLUME = 0

        # FONT
        self.FONT = PIXEL_FONT

    def font(self) -> Font:
        return Font(self.FONT, 100)

    def fontSmall(self) -> Font:
        return Font(self.FONT, 50)
