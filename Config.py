from math import ceil

from pygame.font import Font

from constants import TILE_SIZE, PIXEL_FONT, FONT_SIZE, FONT_SIZE_BIG, FONT_SIZE_HUGE, FONT_SIZE_TINY


class Config:
    def __init__(self) -> None:
        self.WINDOW_WIDTH = 1920
        self.WINDOW_HEIGHT = 1080
        self.TILES_ON_SCREEN_WIDTH = ceil(self.WINDOW_WIDTH / TILE_SIZE + 1)
        self.TILES_ON_SCREEN_HEIGHT = ceil(self.WINDOW_HEIGHT / TILE_SIZE + 1)
        self.savefileName = None

        # MUSIC
        self.MUSIC_VOLUME = 0
        self.SOUNDS_VOLUME = 0

        # FONT
        self.FONT = PIXEL_FONT

        self.fontTiny = Font(PIXEL_FONT, FONT_SIZE_TINY)
        self.font = Font(PIXEL_FONT, FONT_SIZE)
        self.fontBig = Font(PIXEL_FONT, FONT_SIZE_BIG)
        self.fontHuge = Font(PIXEL_FONT, FONT_SIZE_HUGE)

    def setFont(self, fontPath: str):
        self.fontTiny = Font(fontPath, FONT_SIZE_TINY)
        self.font = Font(fontPath, FONT_SIZE)
        self.fontBig = Font(fontPath, FONT_SIZE_BIG)
        self.fontHuge = Font(fontPath, FONT_SIZE_HUGE)
