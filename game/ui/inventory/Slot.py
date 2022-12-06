import pygame.sprite
from pygame import Surface

from config import *
from ui.inventory.items.Item import Item


class Slot(pygame.sprite.Sprite):
    def __init__(self, topleftPosition: pygame.math.Vector2(), item: Item = None):
        super().__init__()
        self.image: Surface = pygame.image.load(f"{ROOT_PATH}/graphics/ui/slot.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = topleftPosition

        self.item = item

    def addItem(self, item: Item) -> None:
        self.item = item

    def removeItem(self) -> None:
        self.item = None

    def use(self):
        if hasattr(self.item, "use"):
            self.item.use()

    def isEmpty(self) -> bool:
        if self.item is None:
            return True
        else:
            return False
