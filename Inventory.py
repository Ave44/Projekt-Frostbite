import pygame
from pygame.surface import Surface

from Item import Item
from Slot import Slot
from game.CameraSpriteGroup import CameraSpriteGroup


class Inventory(pygame.sprite.Sprite):
    def __init__(self,
                 visibleSprites: CameraSpriteGroup,
                 inventoryHeight: int,
                 inventoryWidth: int,
                 selectedItem: Item | None = None):

        super().__init__()
        self._inventoryHeight = inventoryHeight
        self._inventoryWidth = inventoryWidth
        self._selectedItem = selectedItem
        self._inventoryList: list[Slot] = [Slot()] * inventoryWidth * inventoryHeight
        self._isOpened: bool = False

        self._visibleSprites = visibleSprites
        self._image: Surface = pygame.image.load("path_to_image")
        self._rect = self.image.get_rect()
        self._center = pygame.math.Vector2()

    @property
    def selectedItem(self) -> Item | None:
        return self._selectedItem

    @property
    def isOpened(self) -> bool:
        return self._isOpened

    def open(self) -> None:
        self._visibleSprites.add(self)
        self._visibleSprites.add(*self._inventoryList)
        self._isOpened = True

    def close(self) -> None:
        self._visibleSprites.remove(self)
        self._visibleSprites.remove(*self._inventoryList)
        self._isOpened = False

    def addItem(self, item: Item) -> None:
        first: Slot | None = next(filter(lambda slot: (slot.isEmpty()), self._inventoryList), None)
        if first is None and self._selectedItem is not None:
            pos = pygame.mouse.get_pos()
            self._selectedItem.drop(*pos)
            self._selectedItem = item
            return
        if first is None and self._selectedItem is None:
            self._selectedItem = item
            return
        indexOfSlot: int = self._inventoryList.index(first)
        self._inventoryList[indexOfSlot].item = item
        return

    def update(self) -> None:
        pos = pygame.mouse.get_pos()
        if self._selectedItem is not None:
            self._selectedItem.rect.center = pos
            return
        hooveredSlots = [s for s in self._inventoryList if s.rect.collidepoint(pos)]
        for slot in hooveredSlots:
            slot.conditionalUpdate()
        return
