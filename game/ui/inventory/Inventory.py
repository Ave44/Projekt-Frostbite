from config import *
from game.items.Item import Item
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
        self.spriteGroup = spriteGroup

        self.image = pygame.Surface([inventoryWidth * (SLOTSIZE + SLOTGAP) + SLOTGAP, inventoryHeight * (SLOTSIZE + SLOTGAP) + SLOTGAP], pygame.SRCALPHA, 32)
        self.image.fill((50,50,50))
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.slotList: list[Slot] = [Slot(self.calculateSlotPosition(pygame.math.Vector2(x, y), pygame.math.Vector2(self.rect.topleft)))
                                        for y in range(inventoryHeight)
                                        for x in range(inventoryWidth)]


    def calculateSlotPosition(self, index: pygame.math.Vector2(), topleft: pygame.math.Vector2()) -> pygame.math.Vector2():
        return (topleft.x + SLOTGAP + index.x * (SLOTSIZE + SLOTGAP),
                topleft.y + SLOTGAP + index.y * (SLOTSIZE + SLOTGAP))

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
        item.removeFromSpriteGroup()
        
        if emptySlot:
            emptySlot.addItem(item)
        else:
            selectedItem.addItem(item)

    def handleMouseLeftClick(self, mousePos: pygame.math.Vector2(), selectedItem: SelectedItem):
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

    def handleMouseRightClick(self, mousePos: pygame.math.Vector2()):
        if self.isOpen:
            hoveredSlot = next(filter(lambda slot: (slot.rect.collidepoint(mousePos)), self.slotList), None)

            if hoveredSlot:
                hoveredSlot.use()

