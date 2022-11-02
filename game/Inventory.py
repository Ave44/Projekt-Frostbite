import pygame
from pygame.math import Vector2
from pygame.surface import Surface

from Item import Item
from Slot import Slot
from game.CameraSpriteGroup import CameraSpriteGroup


class Inventory(pygame.sprite.Sprite):
    def __init__(self,
                 visibleSprites: CameraSpriteGroup,
                 inventoryHeight: int,
                 inventoryWidth: int,
                 center: Vector2,
                 offset: Vector2,
                 selectedItem: Item | None = None):

        super().__init__()
        self._inventoryHeight = inventoryHeight
        self._inventoryWidth = inventoryWidth
        self._selectedItem = selectedItem
        self._inventoryList: list[Slot] = [Slot(Vector2(x * 32, y * 32) + center - Vector2(inventoryWidth * 16, inventoryHeight * 16) + offset)
                                           for x in range(0, inventoryWidth)
                                           for y in range(0, inventoryHeight)]
        self._isOpened: bool = False

        self._visibleSprites = visibleSprites
        self.image: Surface = pygame.Surface([inventoryWidth * 32, inventoryHeight * 32])
        self.rect = self.image.get_rect()
        self.rect.center = center

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
            self._selectedItem.drop(self.rect.center)
            self._selectedItem = item
            return
        if first is None and self._selectedItem is None:
            self._selectedItem = item
            return
        indexOfSlot: int = self._inventoryList.index(first)
        self._inventoryList[indexOfSlot].addItem(item)
        return

    def conditionalUpdate(self, slot: Slot):
        pass

    def update(self) -> None:
        pos = pygame.mouse.get_pos()
        if self._selectedItem is not None:
            self._selectedItem.rect.center = pos
            return
        hooveredSlots = [s for s in self._inventoryList if s.rect.collidepoint(pos)]
        for slot in hooveredSlots:
            self.conditionalUpdate(slot)
        return


