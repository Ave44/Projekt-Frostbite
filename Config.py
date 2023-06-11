from math import ceil

from pygame import display
from pygame.font import Font

from constants import TILE_SIZE, PIXEL_FONT, FONT_SIZE, FONT_SIZE_BIG, FONT_SIZE_HUGE, FONT_SIZE_TINY


class Config:
    def __init__(self) -> None:
        self.monitorWidth = display.Info().current_w
        self.monitorHeight = display.Info().current_h
        self.window = None
        self.WINDOW_WIDTH = self.monitorWidth
        self.WINDOW_HEIGHT = self.monitorHeight
        self.TILES_ON_SCREEN_WIDTH = ceil(self.WINDOW_WIDTH / TILE_SIZE + 1)
        self.TILES_ON_SCREEN_HEIGHT = ceil(self.WINDOW_HEIGHT / TILE_SIZE + 1)
        self.savefileName = None

        # MUSIC
        self.MUSIC_VOLUME = 0.5
        self.SOUNDS_VOLUME = 0.5

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

    def setWindowSize(self, width: int, height: int):
        self.WINDOW_WIDTH = width
        self.WINDOW_HEIGHT = height
        self.TILES_ON_SCREEN_WIDTH = ceil(self.WINDOW_WIDTH / TILE_SIZE + 1)
        self.TILES_ON_SCREEN_HEIGHT = ceil(self.WINDOW_HEIGHT / TILE_SIZE + 1)