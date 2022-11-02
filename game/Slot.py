import pygame.sprite
from pygame.math import Vector2
from pygame.surface import Surface

from Item import Item


class Slot(pygame.sprite.Sprite):
    def __init__(self, center: Vector2, item: Item = None):
        super().__init__()

        self._image: Surface = pygame.image.load("../graphics/ui/slot.png").convert_alpha()
        self.center = center
        self.rect = self.image.get_rect()

        self._item = item

    @property
    def item(self) -> Item:
        if self.isEmpty():
            raise ValueError("The slot is empty")
        else:
            return self._item

    def addItem(self, item: Item) -> None:
        if self._item is None:
            self._item = item
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
            return False
        else:
            return True
