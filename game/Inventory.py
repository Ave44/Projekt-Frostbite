import pygame

from game.Item import Item
from game.Slot import Slot
from game.CameraSpriteGroup import CameraSpriteGroup


class Inventory(pygame.sprite.Sprite):
    def __init__(self,
                 visibleSprites: CameraSpriteGroup,
                 inventoryHeight: int,
                 inventoryWidth: int,
                 playerCenter: tuple[int, int],):

        super().__init__()
        self._inventoryHeight = inventoryHeight
        self._inventoryWidth = inventoryWidth
        self._selectedItem = None
        self._isOpened: bool = False
        self._playerCenter = playerCenter
        self._offset = (-1280 // 2 + 16 * inventoryWidth + 16, -720 // 2 + 16 * inventoryHeight + 16)
        self._inventoryList: list[Slot] = [Slot(self.__calculateSlotPosition((x, y)))
                                           for x in range(0, inventoryWidth)
                                           for y in range(0, inventoryHeight)]

        self._visibleSprites = visibleSprites
        self.image = pygame.Surface([inventoryWidth * 32, inventoryHeight * 32], pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()

    @property
    def selectedItem(self) -> Item | None:
        return self._selectedItem

    @property
    def isOpened(self) -> bool:
        return self._isOpened

    @property
    def playerCenter(self) -> tuple[int, int]:
        return self._playerCenter

    @playerCenter.setter
    def playerCenter(self, playerCenter: tuple[int, int]) -> None:
        self._playerCenter = playerCenter

        self.rect.center = [self._playerCenter[1] + self._offset[1] - 16,
                            self._playerCenter[1] + self._offset[1] - 16]

        for i, slot in enumerate(self._inventoryList):
            y = i // self._inventoryWidth
            x = i - y * self._inventoryWidth
            slot.rect.center = self.__calculateSlotPosition((x, y))

    def __calculateSlotPosition(self, index: tuple[int, int]) -> tuple[int, int]:
        return (index[0] * 32 + self._playerCenter[0] - self._inventoryWidth * 16 + self._offset[0],
                index[1] * 32 + self._playerCenter[1] - self._inventoryHeight * 16 + self._offset[1])

    def handleOpening(self):
        if self._isOpened:
            self.__close()
        else:
            self.__open()

    def __open(self) -> None:
        self._visibleSprites.add(self)
        self._visibleSprites.add(*self._inventoryList)
        self._isOpened = True

    def __close(self) -> None:
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

    def update(self) -> None:
        pressedMouseKeys = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        hoveredSlot = next(filter(lambda slot: (slot.rect.collidepoint(pos)), self._inventoryList), None)

        if hoveredSlot is None:
            self.__handleNotHoveredState(pos, pressedMouseKeys)
        return self.__handleHoveredState(pos, pressedMouseKeys, hoveredSlot)

    def __handleNotHoveredState(self, mousePos: tuple[int, int], pressedMouseKeys: tuple[bool, bool, bool]):
        if self._selectedItem is None:
            return
        if pressedMouseKeys[0]:
            self._selectedItem.drop(self.rect.center)
            return
        self._selectedItem.rect.center = mousePos
        return

    def __handleHoveredState(self,
                             mousePos: tuple[int, int],
                             pressedMouseKeys: tuple[bool, bool, bool],
                             hoveredSlot: Slot):
        if self._selectedItem is None and (not pressedMouseKeys[0] or pressedMouseKeys[1]):
            return
        if self._selectedItem is None and pressedMouseKeys[0]:
            self._selectedItem = hoveredSlot.item
            hoveredSlot.removeItem()
            return
        if self._selectedItem is None and pressedMouseKeys[1]:
            hoveredSlot.use()
            return
        if not pressedMouseKeys[0]:
            self._selectedItem.rect.center = mousePos
            return
        if hoveredSlot.isEmpty():
            hoveredSlot.addItem(self._selectedItem)
            self._selectedItem = None
            return
        self._selectedItem, hoveredSlot.item = hoveredSlot.item, self._selectedItem
        return


