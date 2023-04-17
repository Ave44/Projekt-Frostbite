from pygame.time import Clock

from Config import Config
from game.LoadedImages import LoadedImages
from game.weathers.domain.Weather import Weather


class Rain(Weather):
    def __init__(self, loadedImages: LoadedImages, clock: Clock, config: Config):
        loadedImages.loadWeatherImages()

        Weather.__init__(self, loadedImages.rain, clock, config, 200)
