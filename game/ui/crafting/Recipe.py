from abc import ABC
from typing import Type

from pygame import Surface, Vector2
from collections import Counter

from game.LoadedImages import LoadedImages
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.items.domain.Item import Item
from game.ui.inventory.Inventory import Inventory
from game.ui.inventory.slot.SelectedItem import SelectedItem


class Recipe(ABC):
    def __init__(self, visibleSprites: CameraSpriteGroup, loadedImages: LoadedImages,
                 itemToCraft: Type[Item], requiredItems: list[Type[Item]], craftImage: Surface) -> None:
        self.visibleSprites = visibleSprites
        self.loadedImages = loadedImages
        self.image = Surface(loadedImages.slot.get_size())
        self.rect = self.image.get_rect()
        self.image.blit(loadedImages.slot, (0, 0))
        self.image.blit(craftImage, (0, 0))
        self.requiredItems = requiredItems
        self.itemToCraft = itemToCraft

        itemDict = Counter(item.__name__ for item in self.requiredItems)
        requirementsStr = ""
        for key, value in itemDict.items():
            requirementsStr += f"{value}x {key}, "
        requirementsStr = requirementsStr[:-2]

        self.cratableMessage = f"Craft from: {requirementsStr}"
        self.uncratableMessage = f"Requires: {requirementsStr}"

    def hoverMessage(self, inventory: Inventory) -> str:
        if inventory.contains(self.requiredItems):
            return self.cratableMessage
        else:
            return self.uncratableMessage

    def craft(self, inventory: Inventory, selectedItem: SelectedItem) -> None:
        if inventory.contains(self.requiredItems):
            inventory.remove(self.requiredItems)
            craftedItem = self.itemToCraft(self.visibleSprites, [0, 0], self.loadedImages)
            inventory.addItem(craftedItem, selectedItem)

    def draw(self, surface: Surface, position: Vector2) -> None:
        surface.blit(self.image, position)
