from game.CameraSpriteGroup import CameraSpriteGroup
from game.item.Item import Item
from game.ui.Slot import Slot
from config import *
from game.ui.UiInterface import UiInterface


class Inventory(pygame.sprite.Sprite, UiInterface):
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
        self._isOpen: bool = False
        self._slotRec = pygame.image.load(os.path.join(ROOT_PATH, "graphics", "ui", "slot.png")).get_size()
        self._windowOffset = (- WINDOW_WIDTH // 2, - WINDOW_HEIGHT // 2)
        self._totalOffset = (self._windowOffset[0] + playerPos[0], self._windowOffset[1] + playerPos[1])
        self._inventoryList: list[Slot] = [Slot(self.__calculateSlotPosition((x, y)))
                                           for x in range(inventoryWidth)
                                           for y in range(inventoryHeight)]

        self.visibleSprites = visibleSprites
        self.image = pygame.Surface([inventoryWidth * self._slotRec[0], inventoryHeight * self._slotRec[1]],
                                    pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()

    @property
    def playerPos(self) -> tuple[int, int]:
        return self._playerPos

    @property
    def selectedItem(self) -> Item:
        return self._selectedItem

    @selectedItem.setter
    def selectedItem(self, item: Item) -> None:
        self._selectedItem = item

    @property
    def isOpen(self) -> bool:
        return self._isOpen

    @property
    def totalOffset(self) -> tuple[int, int]:
        return self._totalOffset

    @property
    def inventoryList(self) -> list[Slot]:
        return self._inventoryList

    @inventoryList.setter
    def inventoryList(self, inventoryList: list[Slot]) -> None:
        if len(inventoryList) == len(self._inventoryList):
            self._inventoryList = inventoryList
        else:
            raise ValueError("Can not set inventory list of different length")

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

    def toggle(self):
        if self._isOpen:
            self.__close()
        else:
            self.__open()

    def __open(self) -> None:
        self.visibleSprites.add(self)
        self.visibleSprites.add(*self._inventoryList)
        self._isOpen = True

    def __close(self) -> None:
        self.visibleSprites.remove(self)
        self.visibleSprites.remove(*self._inventoryList)
        self._isOpen = False

    def addItem(self, item: Item) -> None:
        emptySlotOption: Slot | None = next(filter(lambda slot: (slot.isEmpty()), self._inventoryList), None)
        if emptySlotOption is None and self._selectedItem is not None:
            self._selectedItem.drop(self.playerPos)
            self._selectedItem = item
            return
        if emptySlotOption is None and self._selectedItem is None:
            self._selectedItem = item
            return
        emptySlotOption.addItem(item)
        return

    def __getCalculatedMousePos(self):
        mousePos = pygame.mouse.get_pos()
        calculatedMousePos = (mousePos[0] + self._totalOffset[0],
                              mousePos[1] + self._totalOffset[1])
        return calculatedMousePos

    def update(self) -> None:
        if self._selectedItem is None:
            return

        calculatedMousePos = self.__getCalculatedMousePos()
        self._selectedItem.rect.center = calculatedMousePos
        return

    def handleMouseLeftClick(self):
        calculatedMousePos = self.__getCalculatedMousePos()
        hoveredSlot = next(filter(lambda slot: (slot.rect.collidepoint(calculatedMousePos)), self._inventoryList), None)

        if hoveredSlot is None:
            if self._selectedItem is not None:
                self._selectedItem.drop(self._playerPos)
                self._selectedItem = None
                return
        if self._selectedItem is None and not hoveredSlot.isEmpty():
            self._selectedItem = hoveredSlot.item
            hoveredSlot.removeItem()
            return
        if hoveredSlot.isEmpty() and self._selectedItem is not None:
            hoveredSlot.addItem(self._selectedItem)
            self._selectedItem = None
            return
        if self._isOpen:
            self._selectedItem, hoveredSlot.item = hoveredSlot.item, self._selectedItem
        self.visibleSprites.add(self._selectedItem)
        self._selectedItem.drop(self._playerPos)
        self._selectedItem = None
        return

    def handleMouseRightClick(self):
        calculatedMousePos = self.__getCalculatedMousePos()
        hoveredSlot = next(filter(lambda slot: (slot.rect.collidepoint(calculatedMousePos)), self._inventoryList), None)

        if hoveredSlot is None:
            return
        if self._selectedItem is None:
            hoveredSlot.use()
            return
        return
