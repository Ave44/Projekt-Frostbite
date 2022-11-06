import os.path
from abc import ABC

import pygame.sprite
import shortuuid
from pygame import Surface

from config import ROOT_PATH


class Item(pygame.sprite.Sprite, ABC):
    def __init__(self, name: str, imageFilename: str = None, iconFilename: str = None):
        super().__init__()
        self._id = shortuuid.uuid()
        self._name = name

        self._image = pygame.image.load(
            os.path.join(ROOT_PATH, "graphics", "items", imageFilename)) \
            if imageFilename is not None \
            else pygame.image.load(os.path.join(ROOT_PATH, "graphics", "items", "undefined.png"))
        self._icon = pygame.image.load(
            os.path.join(ROOT_PATH, "graphics", "items", iconFilename)) \
            if iconFilename is not None \
            else pygame.image.load(os.path.join(ROOT_PATH, "graphics", "items", "undefined.png"))
        self.rect = self.image.get_rect()

    @property
    def id(self) -> str:
        return self._id

    @property
    def image(self) -> Surface:
        return self._image

    @image.setter
    def image(self, image: Surface):
        self.image = image
        self.rect = image.get_rect()
        return

    @property
    def icon(self):
        return self.icon

    @icon.setter
    def icon(self, icon: Surface):
        self.icon = icon

    @property
    def name(self) -> str:
        return self._name

    def drop(self, pos: tuple[int, int]) -> None:
        self.remove()
        self.rect.center = pos

    def use(self):
        pass
