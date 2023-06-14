from typing import Type

from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.LoadedImages import LoadedImages
from game.items.Wood import Wood
from game.items.domain.Item import Item
from game.ui.crafting.recipes.domain.Recipe import Recipe


class SwordRecipe(Recipe):
    def __init__(self, visibleSprites: CameraSpriteGroup, loadedImages: LoadedImages):
        Recipe.__init__(self, visibleSprites, loadedImages)
        self.image.blit(loadedImages.sword, (0, 0))
        self.requiredItems = [Wood]

    # @property
    # def requiredItems(self) -> list[Type[Item]]:
    #     return [Wood]
