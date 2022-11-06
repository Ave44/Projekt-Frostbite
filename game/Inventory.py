from game.CameraSpriteGroup import CameraSpriteGroup
from game.Item import Item
from game.Slot import Slot
from config import *


class Inventory(pygame.sprite.Sprite):
    def __init__(self,
                 visibleSprites: CameraSpriteGroup,
                 inventoryHeight: int,
                 inventoryWidth: int,
                 playerPos: tuple[int, int],
                 selectedItem: Item = None):

        super().__init__()
        self._inventoryHeight = inventoryHeight
        self._inventoryWidth = inventoryWidth
        self._playerPos = playerPos
        self._selectedItem = selectedItem
        self._isOpened: bool = False
        self._slotRec = pygame.image.load(os.path.join(ROOT_PATH, "graphics", "ui", "slot.png")).get_size()
        self._windowOffset = (- WINDOW_WIDTH // 2, - WINDOW_HEIGHT // 2)
        self._totalOffset = (self._windowOffset[0] + playerPos[0], self._windowOffset[1] + playerPos[1])
        self._inventoryList: list[Slot] = [Slot(self.__calculateSlotPosition((x, y)))
                                           for x in range(inventoryWidth)
                                           for y in range(inventoryHeight)]

        self.visibleSprites = visibleSprites
        self.image = pygame.Surface([inventoryWidth * self._slotRec[0], inventoryHeight * self._slotRec[1]],
                                    pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()

    @property
    def selectedItem(self) -> Item | None:
        return self._selectedItem

    @property
    def isOpened(self) -> bool:
        return self._isOpened

    def updatePos(self, playerCenter: tuple[int, int]) -> None:
        self._playerPos = playerCenter
        self._totalOffset = (self._windowOffset[0] + playerCenter[0], self._windowOffset[1] + playerCenter[1])
        self.rect.topleft = self._totalOffset

        for i, slot in enumerate(self._inventoryList):
            y = i // self._inventoryWidth
            x = i - y * self._inventoryWidth
            slot.rect.center = self.__calculateSlotPosition((x, y))

    def __calculateSlotPosition(self, index: tuple[int, int]) -> tuple[int, int]:
        return ((index[0] + 0.5) * self._slotRec[0] + self._totalOffset[0],
                (index[1] + 0.5) * self._slotRec[1] + self._totalOffset[1])

    def handleOpening(self):
        if self._isOpened:
            self.__close()
        else:
            self.__open()

    def __open(self) -> None:
        self.visibleSprites.add(self)
        self.visibleSprites.add(*self._inventoryList)
        self.visibleSprites.add(*[slot.item for slot in self._inventoryList if not slot.isEmpty()])
        self._isOpened = True

    def __close(self) -> None:
        self.visibleSprites.remove(self)
        self.visibleSprites.remove(*self._inventoryList)
        self.visibleSprites.remove(*[slot.item for slot in self._inventoryList if not slot.isEmpty()])
        self._isOpened = False

    def addItem(self, item: Item) -> None:
        emptySlotOption: Slot | None = next(filter(lambda slot: (slot.isEmpty()), self._inventoryList), None)
        if emptySlotOption is None and self._selectedItem is not None:
            self._selectedItem.drop(self.rect.center)
            self._selectedItem = item
            return
        if emptySlotOption is None and self._selectedItem is None:
            self._selectedItem = item
            return
        emptySlotOption.addItem(item)
        return

    def update(self) -> None:
        pressedMouseKeys = pygame.mouse.get_pressed()

        mousePos = pygame.mouse.get_pos()
        calculatedMousePos = (mousePos[0] + self._totalOffset[0],
                              mousePos[1] + self._totalOffset[1])

        hoveredSlot = next(filter(lambda slot: (slot.rect.collidepoint(calculatedMousePos)), self._inventoryList), None)

        if hoveredSlot is None:
            return self.__handleNotHoveredState(mousePos, pressedMouseKeys)
        return self.__handleHoveredState(mousePos, pressedMouseKeys, hoveredSlot)

    def __handleNotHoveredState(self, mousePos: tuple[int, int],
                                pressedMouseKeys: tuple[bool, bool, bool]) -> None:
        if self._selectedItem is None:
            return
        if pressedMouseKeys[0]:
            self._selectedItem.drop(self._playerPos)
            self._selectedItem = None
            return
        self._selectedItem.rect.center = (mousePos[0] + self._totalOffset[0],
                                          mousePos[1] + self._totalOffset[1])
        return

    def __handleHoveredState(self,
                             mousePos: tuple[int, int],
                             pressedMouseKeys: tuple[bool, bool, bool],
                             hoveredSlot: Slot) -> None:
        if self._selectedItem is None and (not pressedMouseKeys[0] or pressedMouseKeys[1]):
            return
        if self._selectedItem is None and pressedMouseKeys[0] and not hoveredSlot.isEmpty():
            self._selectedItem = hoveredSlot.item
            hoveredSlot.removeItem()
            return
        if self._selectedItem is None and pressedMouseKeys[1]:
            hoveredSlot.use()
            return
        if not pressedMouseKeys[0]:
            self._selectedItem.rect.center = (mousePos[0] + self._totalOffset[0],
                                              mousePos[1] + self._totalOffset[1])
            return
        if hoveredSlot.isEmpty() and self._selectedItem is not None:
            hoveredSlot.addItem(self._selectedItem)
            self._selectedItem = None
            return
        self._selectedItem, hoveredSlot.item = hoveredSlot.item, self._selectedItem
        return
