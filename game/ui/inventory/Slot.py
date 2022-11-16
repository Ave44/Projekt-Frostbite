import pygame.sprite
from pygame import Surface

from config import *
from game.item.Item import Item


class Slot(pygame.sprite.Sprite):
    def __init__(self, center: pygame.math.Vector2(), item: Item = None):
        super().__init__()
        self.image: Surface = pygame.image.load(f"{ROOT_PATH}/graphics/ui/slot.png")
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.item = item


    def addItem(self, item: Item) -> None:
        if self.item is None:
            self.item = item
            self.item.rect.center = self.rect.center
            return
        raise ValueError("The slot is taken")

    def removeItem(self) -> None:
        if self.item is None:
            raise ValueError("The slot is empty")
        self.item = None
        return

    def use(self):
        if self.item is None:
            raise ValueError("The slot is empty")
        self.item.use()
        return

    def isEmpty(self) -> bool:
        if self.item is None:
            return True
        else:
            return False

    def update(self) -> None:
        if self.item is not None:
            self.item.rect.center = self.rect.center
