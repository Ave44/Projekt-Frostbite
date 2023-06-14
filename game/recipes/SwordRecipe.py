from typing import Type

from pygame import Surface

from game.LoadedImages import LoadedImages
from game.items.Wood import Wood
from game.items.domain.Item import Item
from game.recipes.domain.Recipe import Recipe


class SwordRecipe(Recipe):
    def __init__(self, loadedImages: LoadedImages):
        self.image = Surface(loadedImages.slot.get_size())
        self.image.blit(loadedImages.slot, (0, 0))
        self.image.blit(loadedImages.sword, (0, 0))

    @property
    def requiredItems(self) -> list[Type[Item]]:
        return [Wood]
