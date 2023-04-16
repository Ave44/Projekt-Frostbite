from math import ceil
from constants import TILE_SIZE

class Config:
    def __init__(self) -> None:
        self.WINDOW_WIDTH = 1920
        self.WINDOW_HEIGHT = 1080
        self.TILES_ON_SCREEN_WIDTH = ceil(self.WINDOW_WIDTH / TILE_SIZE + 1)
        self.TILES_ON_SCREEN_HEIGHT = ceil(self.WINDOW_HEIGHT / TILE_SIZE + 1)

        # MUSIC
        self.MUSIC_VOLUME = 0 #.5
        self.SOUNDS_VOLUME = 0
