from collections import Counter
from typing import Type

from pygame import Surface
from pygame.math import Vector2
from pygame.sprite import Sprite, Group
from constants import BG_COLOR, SLOT_GAP, SLOT_SIZE
from game.ui.inventory.slot.Slot import Slot
from game.items.domain.Item import Item
from game.ui.inventory.slot.SelectedItem import SelectedItem
from game.LoadedImages import LoadedImages


class Inventory(Sprite):
    def __init__(self,
                 spriteGroup: Group,
                 inventoryHeight: int,
                 inventoryWidth: int,
                 center: Vector2,
                 loadedImages: LoadedImages):

        super().__init__()
        self.inventoryHeight = inventoryHeight
        self.inventoryWidth = inventoryWidth
        self.isOpen: bool = False
        self.spriteGroup = spriteGroup
        self.image = Surface(
            [inventoryWidth * (SLOT_SIZE + SLOT_GAP) + SLOT_GAP,
             inventoryHeight * (SLOT_SIZE + SLOT_GAP) + SLOT_GAP])
        self.image.fill(BG_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.slotList: list[Slot] = [
            Slot(self.calculateSlotPosition(Vector2(x, y), Vector2(self.rect.topleft)), loadedImages.slot)
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

    def checkIfContains(self, items: list[Type[Item]]) -> bool:
        inventoryDict = Counter(type(slot.item) for slot in self.slotList)

        for item in items:
            dictItemValue = inventoryDict.get(item)
            if dictItemValue and dictItemValue > 0:
                inventoryDict[item] = inventoryDict[item] - 1
            else:
                return False
        return True

    def remove(self, items: list[Type[Item]]) -> None:
        for item in items:
            for slot in self.slotList:
                if isinstance(slot.item, item):
                    slot.removeItem()
    def getSaveData(self) -> dict:
        slotsItemData = []
        for slot in self.slotList:
            slotsItemData.append(slot.getItemId())
        return {'slotsItemData': slotsItemData}
