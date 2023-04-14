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

        self.item = item
        self.type = type

    def addItem(self, item: Item) -> None:
        self.item = item
        item.Slot = self

    def removeItem(self) -> None:
        self.item = None

    def isEmpty(self) -> bool:
        if self.item is None:
            return True
        else:
            return False
        
    def handleMouseLeftClick(self, player):
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

    def handleMouseRightClick(self, player):
        if hasattr(self.item, "use"):
            self.item.use(player)
            self.item.kill()
            self.removeItem()
        elif isinstance(self.item, Tool):
            if self.type == Tool and self.item:
                player.inventory.addItem(self.item)
                self.removeItem()
            else:
                pass
            
        elif isinstance(self.item, Armor):
            pass
