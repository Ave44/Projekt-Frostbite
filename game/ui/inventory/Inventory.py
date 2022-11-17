from config import *
from game.item.Item import Item
from game.ui.SelectedItem import SelectedItem
from game.ui.inventory.Slot import Slot


class Inventory(pygame.sprite.Sprite):
    def __init__(self,
                 spriteGroup: pygame.sprite.Group,
                 inventoryHeight: int,
                 inventoryWidth: int,
                 center: pygame.math.Vector2()):

        super().__init__()
        self.inventoryHeight = inventoryHeight
        self.inventoryWidth = inventoryWidth
        self.isOpen: bool = False
        self.slotRectSize = pygame.image.load(f"{ROOT_PATH}/graphics/ui/slot.png").get_size()[0]
        self.spriteGroup = spriteGroup

        self.image = pygame.Surface([inventoryWidth * (self.slotRectSize + SLOTGAP) + SLOTGAP, inventoryHeight * (self.slotRectSize + SLOTGAP) + SLOTGAP], pygame.SRCALPHA, 32)
        self.image.fill((50,50,50))
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.slotList: list[Slot] = [Slot(self.calculateSlotPosition(pygame.math.Vector2(x, y), pygame.math.Vector2(self.rect.topleft)))
                                        for x in range(inventoryWidth)
                                        for y in range(inventoryHeight)]


    def calculateSlotPosition(self, index: pygame.math.Vector2(), topleft: pygame.math.Vector2()) -> pygame.math.Vector2():
        return (index.x * (self.slotRectSize + SLOTGAP) + SLOTGAP + topleft.x,
                index.y * (self.slotRectSize + SLOTGAP) + SLOTGAP + topleft.y)

    def toggle(self):
        if self.isOpen:
            self.close()
        else:
            self.open()

    def open(self) -> None:
        self.spriteGroup.add(self)
        self.spriteGroup.add(*self.slotList)
        self.isOpen = True

    def close(self) -> None:
        self.spriteGroup.remove(self)
        self.spriteGroup.remove(*self.slotList)
        self.isOpen = False

    def addItem(self, item: Item, selectedItem: SelectedItem) -> None:
        emptySlotOption: Slot | None = next(filter(lambda slot: (slot.isEmpty()), self.slotList), None)
        if emptySlotOption is None and not selectedItem.isEmpty():
            selectedItem.drop()
            selectedItem = item
            return
        if emptySlotOption is None and selectedItem.isEmpty():
            selectedItem = item
            return
        emptySlotOption.addItem(item)
        return

    def handleMouseLeftClick(self, mousePos: pygame.math.Vector2(), selectedItem: SelectedItem):
        hoveredSlot = next(filter(lambda slot: (slot.rect.collidepoint(mousePos)), self.slotList), None)
        if hoveredSlot is None:
            if self.isOpen and not selectedItem.isEmpty():
                selectedItem.drop()
                self.spriteGroup.add(selectedItem.item)
                selectedItem.removeItem()
                return
            return
        if self.isOpen and selectedItem.isEmpty() and not hoveredSlot.isEmpty():
            selectedItem.item = hoveredSlot.item
            hoveredSlot.removeItem()
            return
        if self.isOpen and hoveredSlot.isEmpty() and not selectedItem.isEmpty():
            hoveredSlot.addItem(selectedItem.item)
            selectedItem.removeItem()
            return
        if self.isOpen and not selectedItem.isEmpty():
            selectedItem.item, hoveredSlot.item = hoveredSlot.item, selectedItem.item
            return
        if not selectedItem.isEmpty():
            selectedItem.drop()
            self.spriteGroup.add(selectedItem.item)
            selectedItem.removeItem()
            return

    def handleMouseRightClick(self, mousePos: pygame.math.Vector2(), selectedItem: SelectedItem):
        hoveredSlot = next(filter(lambda slot: (slot.rect.collidepoint(mousePos)), self.slotList), None)

        if hoveredSlot is None:
            return
        if self.isOpen and selectedItem.isEmpty():
            hoveredSlot.use()
            return
