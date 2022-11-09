from config import *
from game.CameraSpriteGroup import CameraSpriteGroup
from game.item.Item import Item
from game.ui.SelectedItem import SelectedItem
from game.ui.inventory.Slot import Slot


class Inventory(pygame.sprite.Sprite):
    def __init__(self,
                 visibleSprites: CameraSpriteGroup,
                 inventoryHeight: int,
                 inventoryWidth: int,
                 uiPos: tuple[int, int],
                 selectedItem: SelectedItem):

        super().__init__()
        self._inventoryHeight = inventoryHeight
        self._inventoryWidth = inventoryWidth
        self.selectedItem = selectedItem
        self._isOpen: bool = False
        self._slotRec = pygame.image.load(os.path.join(ROOT_PATH, "graphics", "ui", "slot.png")).get_size()

        self.visibleSprites = visibleSprites
        self.image = pygame.Surface([inventoryWidth * self._slotRec[0], inventoryHeight * self._slotRec[1]],
                                    pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()

        self._windowPos = (0, 0)
        self.rect.topleft = (uiPos[0] + self._windowPos[0], uiPos[1] + self._windowPos[1])
        self._inventoryList: list[Slot] = [Slot(self.__calculateSlotPosition((x, y), self.rect.topleft))
                                           for x in range(inventoryWidth)
                                           for y in range(inventoryHeight)]

    @property
    def isOpen(self) -> bool:
        return self._isOpen

    @property
    def inventoryList(self) -> list[Slot]:
        return self._inventoryList

    @inventoryList.setter
    def inventoryList(self, inventoryList: list[Slot]) -> None:
        if len(inventoryList) == len(self._inventoryList):
            self._inventoryList = inventoryList
        else:
            raise ValueError("Can not set inventory list of different length")

    def changePos(self, newPos: tuple[int, int]) -> None:
        updatedPos = (self._windowPos[0] + newPos[0], self._windowPos[1] + newPos[1])
        self.rect.topleft = updatedPos

        for i, slot in enumerate(self._inventoryList):
            y = i // self._inventoryWidth
            x = i - y * self._inventoryWidth
            slot.rect.center = self.__calculateSlotPosition((x, y), updatedPos)

    def __calculateSlotPosition(self, index: tuple[int, int], newPos: tuple[int, int]) -> tuple[int, int]:
        return (index[0] * self._slotRec[0] + self._slotRec[0] // 2 + newPos[0],
                index[1] * self._slotRec[1] + self._slotRec[0] // 2 + newPos[1])

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
        if emptySlotOption is None and not self.selectedItem.isEmpty():
            self.selectedItem.drop()
            self.selectedItem = item
            return
        if emptySlotOption is None and self.selectedItem.isEmpty():
            self.selectedItem = item
            return
        emptySlotOption.addItem(item)
        return

    def handleMouseLeftClick(self, mousePos: tuple[int, int]):
        hoveredSlot = next(filter(lambda slot: (slot.rect.collidepoint(mousePos)), self._inventoryList), None)
        if hoveredSlot is None:
            if self._isOpen and not self.selectedItem.isEmpty():
                self.selectedItem.drop()
                self.visibleSprites.add(self.selectedItem.item)
                self.selectedItem.removeItem()
                return
            return
        if self._isOpen and self.selectedItem.isEmpty() and not hoveredSlot.isEmpty():
            self.selectedItem.item = hoveredSlot.item
            hoveredSlot.removeItem()
            return
        if self._isOpen and hoveredSlot.isEmpty() and not self.selectedItem.isEmpty():
            hoveredSlot.addItem(self.selectedItem.item)
            self.selectedItem.removeItem()
            return
        if self._isOpen and not self.selectedItem.isEmpty():
            self.selectedItem.item, hoveredSlot.item = hoveredSlot.item, self.selectedItem.item
            return
        if not self.selectedItem.isEmpty():
            self.selectedItem.drop()
            self.visibleSprites.add(self.selectedItem.item)
            self.selectedItem.removeItem()
            return

    def handleMouseRightClick(self, mousePos: tuple[int, int]):
        hoveredSlot = next(filter(lambda slot: (slot.rect.collidepoint(mousePos)), self._inventoryList), None)

        if hoveredSlot is None:
            return
        if self._isOpen and self.selectedItem.isEmpty():
            hoveredSlot.use()
            return
