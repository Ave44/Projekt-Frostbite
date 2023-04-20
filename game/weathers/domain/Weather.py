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
        return list(map(lambda i: self.scaleImageToFitWindow(i), images))

    def scaleImageToFitWindow(self, image: Surface):

        imageWidth = image.get_width()
        imageHeight = image.get_height()
        numberOfImagesToCoverScreenWidth = ceil(self.config.WINDOW_WIDTH / imageWidth)
        numberOfImagesToCoverScreenHeight = ceil(self.config.WINDOW_HEIGHT / imageHeight)
        scaledImage = Surface((imageWidth * numberOfImagesToCoverScreenWidth, imageHeight * numberOfImagesToCoverScreenHeight), SRCALPHA)

        for x in range(0, numberOfImagesToCoverScreenWidth):
            xWidth = x * imageWidth
            for y in range(0, numberOfImagesToCoverScreenHeight):
                scaledImage.blit(image, (xWidth, y * imageHeight))
        return scaledImage

    @staticmethod
    def expandImages(images: list[Surface]) -> list[Surface]:
        bgImages = []
        for image in images:
            imageWidth = image.get_width()
            imageHeight = image.get_height()
            bgImage = Surface((imageWidth * 2, imageHeight * 2), SRCALPHA)
            for x in range(0, 2):
                for y in range(0, 2):
                    bgImage.blit(image, (x * imageWidth, y * imageHeight))
            bgImages.append(bgImage)
        return bgImages
