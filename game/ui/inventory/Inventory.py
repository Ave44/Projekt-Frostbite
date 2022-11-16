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
                 uiPos: pygame.math.Vector2(),
                 selectedItem: SelectedItem):

        super().__init__()
        self.inventoryHeight = inventoryHeight
        self.inventoryWidth = inventoryWidth
        self.selectedItem = selectedItem
        self.isOpen: bool = False
        self.slotRec = pygame.image.load(f"{ROOT_PATH}/graphics/ui/slot.png").get_size()

        self.visibleSprites = visibleSprites
        self.image = pygame.Surface([inventoryWidth * self.slotRec[0], inventoryHeight * self.slotRec[1]], pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()

        self.windowPos = (0, 0)
        self.rect.topleft = (uiPos[0] + self.windowPos[0], uiPos[1] + self.windowPos[1])
        self.inventoryList: list[Slot] = [Slot(self.calculateSlotPosition((x, y), self.rect.topleft))
                                           for x in range(inventoryWidth)
                                           for y in range(inventoryHeight)]


    def inventoryList(self, inventoryList: list[Slot]) -> None:
        if len(inventoryList) == len(self.inventoryList):
            self.inventoryList = inventoryList
        else:
            raise ValueError("Can not set inventory list of different length")

    def changePos(self, newPos: pygame.math.Vector2()) -> None:
        updatedPos = (self.windowPos[0] + newPos[0], self.windowPos[1] + newPos[1])
        self.rect.topleft = updatedPos

        for i, slot in enumerate(self.inventoryList):
            y = i // self.inventoryWidth
            x = i - y * self.inventoryWidth
            slot.rect.center = self.calculateSlotPosition((x, y), updatedPos)

    def calculateSlotPosition(self, index: pygame.math.Vector2(), newPos: pygame.math.Vector2()) -> pygame.math.Vector2():
        return (index[0] * self.slotRec[0] + self.slotRec[0] // 2 + newPos[0],
                index[1] * self.slotRec[1] + self.slotRec[0] // 2 + newPos[1])

    def toggle(self):
        if self.isOpen:
            self.close()
        else:
            self.open()

    def open(self) -> None:
        self.visibleSprites.add(self)
        self.visibleSprites.add(*self.inventoryList)
        self.isOpen = True

    def close(self) -> None:
        self.visibleSprites.remove(self)
        self.visibleSprites.remove(*self.inventoryList)
        self.isOpen = False

    def addItem(self, item: Item) -> None:
        emptySlotOption: Slot | None = next(filter(lambda slot: (slot.isEmpty()), self.inventoryList), None)
        if emptySlotOption is None and not self.selectedItem.isEmpty():
            self.selectedItem.drop()
            self.selectedItem = item
            return
        if emptySlotOption is None and self.selectedItem.isEmpty():
            self.selectedItem = item
            return
        emptySlotOption.addItem(item)
        return

    def handleMouseLeftClick(self, mousePos: pygame.math.Vector2()):
        hoveredSlot = next(filter(lambda slot: (slot.rect.collidepoint(mousePos)), self.inventoryList), None)
        if hoveredSlot is None:
            if self.isOpen and not self.selectedItem.isEmpty():
                self.selectedItem.drop()
                self.visibleSprites.add(self.selectedItem.item)
                self.selectedItem.removeItem()
                return
            return
        if self.isOpen and self.selectedItem.isEmpty() and not hoveredSlot.isEmpty():
            self.selectedItem.item = hoveredSlot.item
            hoveredSlot.removeItem()
            return
        if self.isOpen and hoveredSlot.isEmpty() and not self.selectedItem.isEmpty():
            hoveredSlot.addItem(self.selectedItem.item)
            self.selectedItem.removeItem()
            return
        if self.isOpen and not self.selectedItem.isEmpty():
            self.selectedItem.item, hoveredSlot.item = hoveredSlot.item, self.selectedItem.item
            return
        if not self.selectedItem.isEmpty():
            self.selectedItem.drop()
            self.visibleSprites.add(self.selectedItem.item)
            self.selectedItem.removeItem()
            return

    def handleMouseRightClick(self, mousePos: pygame.math.Vector2()):
        hoveredSlot = next(filter(lambda slot: (slot.rect.collidepoint(mousePos)), self.inventoryList), None)

        if hoveredSlot is None:
            return
        if self.isOpen and self.selectedItem.isEmpty():
            hoveredSlot.use()
            return
