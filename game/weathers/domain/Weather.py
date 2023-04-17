from abc import ABC

from pygame import Surface, SRCALPHA
from pygame.time import Clock
from pygame.transform import scale

from Config import Config
from game.objects.domain.AnimatedObject import AnimatedObject


class Weather(ABC, AnimatedObject):

    def __init__(self, images: list[Surface], clock: Clock, config: Config, timeBetweenFramesMS):
        self.config = config
        scaledImages = self.scaleImagesToFitWindow(images)
        weatherImages = self.expandImages(scaledImages)
        AnimatedObject.__init__(self, weatherImages, clock, timeBetweenFramesMS)

    def scaleImagesToFitWindow(self, images: list[Surface]) -> list[Surface]:
        return list(map(lambda i: scale(i, (self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT)), images))

    def expandImages(self, images: list[Surface]) -> list[Surface]:
        bgImages = []
        for image in images:
            bgImage = Surface((self.config.WINDOW_WIDTH * 3, self.config.WINDOW_HEIGHT * 3), SRCALPHA)
            for x in range(0, 3):
                for y in range(0, 3):
                    bgImage.blit(image, (x * self.config.WINDOW_WIDTH, y * self.config.WINDOW_HEIGHT))
            bgImages.append(bgImage)
        return bgImages
