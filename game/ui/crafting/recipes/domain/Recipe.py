from abc import ABC
from typing import Type

from pygame import Surface, Vector2

from game.LoadedImages import LoadedImages
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.items.domain.Item import Item
from game.ui.inventory.Inventory import Inventory
from game.ui.inventory.slot.SelectedItem import SelectedItem


class Recipe(ABC):
    def __init__(self, visibleSprites: CameraSpriteGroup, loadedImages: LoadedImages) -> None:
        self.visibleSprites = visibleSprites
        self.loadedImages = loadedImages
        self.image = Surface(loadedImages.slot.get_size())
        self.image.blit(loadedImages.slot, (0, 0))
        self.rect = self.image.get_rect()

        self.requiredItems: list[Type[Item]]
        self.itemToCraft: Item
        self.requirements = str

    def hoverMessage(self, inventory: Inventory) -> str:
        if inventory.contains(self.requiredItems):
            return self.cratablMessage
        else:
            return self.uncratablMessage

    def craft(self, inventory: Inventory, selectedItem: SelectedItem) -> None:
        if inventory.contains(self.requiredItems):
            inventory.remove(self.requiredItems)
            craftedItem = self.itemToCraft(self.visibleSprites, [0, 0], self.loadedImages)
            inventory.addItem(craftedItem, selectedItem)

    def draw(self, surface: Surface, position: Vector2) -> None:
        surface.blit(self.image, position)
