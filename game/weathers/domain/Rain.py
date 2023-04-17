from pygame import Surface, SRCALPHA
from pygame.time import Clock
from pygame.transform import scale

from Config import Config
from game.LoadedImages import LoadedImages
from game.objects.domain.AnimatedObject import AnimatedObject


class Rain(AnimatedObject):
    def __init__(self, loadedImages: LoadedImages, clock: Clock, config: Config):
        loadedImages.loadWeatherImages()
        images = list(map(lambda i: scale(i, (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)), loadedImages.rain))
        bgImages = []
        for image in images:
            bgImage = Surface((config.WINDOW_WIDTH * 3, config.WINDOW_HEIGHT * 3), SRCALPHA)
            for x in range(0, 3):
                for y in range(0, 3):
                    bgImage.blit(image, (x * config.WINDOW_WIDTH, y * config.WINDOW_HEIGHT))
            print(bgImage.get_size())
            bgImages.append(bgImage)

        AnimatedObject.__init__(self, bgImages, clock, 200)