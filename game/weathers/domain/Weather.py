from abc import ABC
from math import ceil

from pygame import Surface, SRCALPHA
from pygame.time import Clock

from Config import Config
from game.objects.domain.AnimatedObject import AnimatedObject


class Weather(ABC, AnimatedObject):

    def __init__(self, images: list[Surface], clock: Clock, config: Config, timeBetweenFramesMs: int):
        self.config = config
        scaledImages = self.scaleImagesToFitWindow(images)
        weatherImages = self.expandImages(scaledImages)
        AnimatedObject.__init__(self, weatherImages, clock, timeBetweenFramesMs)

    def scaleImagesToFitWindow(self, images: list[Surface]) -> list[Surface]:
        return list(map(lambda i: self.scaleImage(i), images))

    def scaleImage(self, image: Surface):
        scaledImage = Surface((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT), SRCALPHA)

        imageWidth = image.get_width()
        imageHeight = image.get_height()
        for x in range(0, ceil(self.config.WINDOW_WIDTH / imageWidth)):
            xWidth = x * imageWidth
            for y in range(0, ceil(self.config.WINDOW_HEIGHT / imageHeight)):
                scaledImage.blit(image, (xWidth, y * imageHeight))
        return scaledImage

    def expandImages(self, images: list[Surface]) -> list[Surface]:
        bgImages = []
        for image in images:
            bgImage = Surface((self.config.WINDOW_WIDTH * 2, self.config.WINDOW_HEIGHT * 2), SRCALPHA)
            for x in range(0, 2):
                for y in range(0, 2):
                    bgImage.blit(image, (x * self.config.WINDOW_WIDTH, y * self.config.WINDOW_HEIGHT))
            bgImages.append(bgImage)
        return bgImages
