from abc import ABC, abstractmethod
from typing import Type

from pygame import Surface, Vector2

from game.LoadedImages import LoadedImages
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.items.domain.Item import Item
from game.ui.inventory.Inventory import Inventory


class Recipe(ABC):
    def __init__(self, visibleSprites: CameraSpriteGroup, loadedImages: LoadedImages) -> None:
        self.visibleSprites = visibleSprites
        self.loadedImages = loadedImages
        self.image = Surface(loadedImages.slot.get_size())
        self.image.blit(loadedImages.slot, (0, 0))
        self.requiredItems: list[Type[Item]]
        self.itemToCraft: Item

    # @property
    # @abstractmethod
    # def requiredItems(self) -> list[Type[Item]]:
    #     pass

    def craft(self, inventory: Inventory) -> None:
        craftedItem = self.itemToCraft(self.visibleSprites, [0, 0], self.loadedImages)
        inventory.addItem(craftedItem)

    def draw(self, surface: Surface, position: Vector2) -> None:
        surface.blit(self.image, position)
