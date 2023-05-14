from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.entities.Player import Player

from pygame import Surface
from pygame.sprite import Sprite
from pygame.math import Vector2

from game.items.domain.Item import Item
from game.items.domain.Tool import Tool
from game.items.domain.Armor import Armor
from typing import Type


class Slot(Sprite):
    def __init__(self, topleftPosition: Vector2, image: Surface, item: Item = None, type: Type = Item):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = topleftPosition

        self.item: Item | None = item
        self.type = type

    def addItem(self, item: Item) -> None:
        self.item = item

    def removeItem(self) -> None:
        self.item = None

    def isEmpty(self) -> bool:
        if self.item is None:
            return True
        else:
            return False

    def handleMouseLeftClick(self, player: Player):
        selectedItem = player.selectedItem
        if self.isEmpty() and not selectedItem.isEmpty() and isinstance(selectedItem.item, self.type):
            self.addItem(selectedItem.item)
            selectedItem.removeItem()

        elif not self.isEmpty() and selectedItem.isEmpty():
            selectedItem.addItem(self.item)
            self.removeItem()

        elif not self.isEmpty() and not selectedItem.isEmpty() and isinstance(selectedItem.item, self.type):
            slotItem = self.item
            self.addItem(selectedItem.item)
            selectedItem.removeItem()
            selectedItem.addItem(slotItem)

    def handleMouseRightClick(self, player: Player):
        if hasattr(self.item, "use"):
            self.item.use(player)
            self.item.kill()
            self.removeItem()
        elif isinstance(self.item, Tool):
            self.swapEquipment(Tool, player.handSlot, player)
        elif isinstance(self.item, Armor):
            self.swapEquipment(Armor, player.bodySlot, player)

    def swapEquipment(self, type: Type, destSlot: Slot, player: Player):
        if self.type == type and self.item:
            player.inventory.addItem(self.item, player.selectedItem)
            self.removeItem()
        else:
            if destSlot.isEmpty():
                destSlot.addItem(self.item)
                self.removeItem()
            else:
                slotItem = self.item
                self.addItem(destSlot.item)
                destSlot.addItem(slotItem)

    def reduceItemDurability(self):
        self.item.reduceDurability()
        if self.item.currDurability <= 0:
            self.removeItem()

    def getItemId(self):
        if not self.isEmpty():
            return self.item.id
        return None