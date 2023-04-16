from pygame import Surface, SRCALPHA
from pygame.math import Vector2
from pygame.sprite import Sprite, Group
from constants import BG_COLOR, SLOT_GAP, SLOT_SIZE
from game.ui.inventory.slot.Slot import Slot
from game.items.domain.Item import Item
from game.ui.inventory.slot.SelectedItem import SelectedItem


class Inventory(Sprite):
    def __init__(self,
                 spriteGroup: Group,
                 inventoryHeight: int,
                 inventoryWidth: int,
                 center: Vector2):

        super().__init__()
        self.inventoryHeight = inventoryHeight
        self.inventoryWidth = inventoryWidth
        self.isOpen: bool = False
        self.spriteGroup = spriteGroup
        self.image = Surface(
            [inventoryWidth * (SLOT_SIZE + SLOT_GAP) + SLOT_GAP, inventoryHeight * (SLOT_SIZE + SLOT_GAP) + SLOT_GAP],
            SRCALPHA, 32)
        self.image.fill(BG_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.slotList: list[Slot] = [
            Slot(self.calculateSlotPosition(Vector2(x, y), Vector2(self.rect.topleft)))
            for y in range(inventoryHeight)
            for x in range(inventoryWidth)]

    def calculateSlotPosition(self, index: Vector2, topleft: Vector2) -> Vector2:
        return Vector2((topleft.x + SLOT_GAP + index.x * (SLOT_SIZE + SLOT_GAP),
                        topleft.y + SLOT_GAP + index.y * (SLOT_SIZE + SLOT_GAP)))

    def toggle(self):
        if self.isOpen:
            self.close()
        else:
            self.open()

    def open(self) -> None:
        self.spriteGroup.add(self, *self.slotList)
        self.isOpen = True

    def close(self) -> None:
        self.spriteGroup.remove(self, *self.slotList)
        self.isOpen = False

    def addItem(self, item: Item, selectedItem: SelectedItem) -> None:
        emptySlot: Slot | None = next(filter(lambda slot: (slot.isEmpty()), self.slotList), None)
        item.hide()

        if emptySlot:
            emptySlot.addItem(item)
        else:
            selectedItem.addItem(item)

    def handleMouseLeftClick(self, mousePos: Vector2, selectedItem: SelectedItem):
        if self.isOpen:
            hoveredSlot = next(filter(lambda slot: (slot.rect.collidepoint(mousePos)), self.slotList), None)

            if hoveredSlot:
                if hoveredSlot.isEmpty() and not selectedItem.isEmpty():
                    hoveredSlot.addItem(selectedItem.item)
                    selectedItem.removeItem()

                elif not hoveredSlot.isEmpty() and selectedItem.isEmpty():
                    selectedItem.addItem(hoveredSlot.item)
                    hoveredSlot.removeItem()

                elif not hoveredSlot.isEmpty() and not selectedItem.isEmpty():
                    slotItem = hoveredSlot.item
                    hoveredSlot.addItem(selectedItem.item)
                    selectedItem.removeItem()
                    selectedItem.addItem(slotItem)

    def handleMouseRightClick(self, mousePos: Vector2):
        if self.isOpen:
            hoveredSlot = next(filter(lambda slot: (slot.rect.collidepoint(mousePos)), self.slotList), None)

            if hoveredSlot:
                hoveredSlot.use()
