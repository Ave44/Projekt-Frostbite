import os

import pygame.sprite
from pygame import Surface

from config import *
from game.item.Item import Item


class Slot(pygame.sprite.Sprite):
    def __init__(self, center: tuple[int, int], item: Item = None):
        super().__init__()
        self.image: Surface = pygame.image.load(os.path.join(ROOT_PATH, "graphics", "ui", "slot.png"))
        self.rect = self.image.get_rect()
        self.rect.center = center

        self._item = item

    @property
    def item(self) -> Item:
        return self._item

    @item.setter
    def item(self, item: Item):
        self._item = item

    def addItem(self, item: Item) -> None:
        if self._item is None:
            self._item = item
            self._item.rect.center = self.rect.center
            return
        raise ValueError("The slot is taken")

    def removeItem(self) -> None:
        if self._item is None:
            raise ValueError("The slot is empty")
        self._item = None
        return

    def use(self):
        if self._item is None:
            raise ValueError("The slot is empty")
        self._item.use()
        return

    def isEmpty(self) -> bool:
        if self.item is None:
            return True
        else:
            return False

    def update(self) -> None:
        if self._item is not None:
            self._item.rect.center = self.rect.center
