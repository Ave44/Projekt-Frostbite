from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.LoadedImages import LoadedImages
from game.ui.crafting.recipes.domain.Recipe import Recipe
from game.items.Sword import Sword
from game.items.Wood import Wood
from game.items.SharpRock import SharpRock
from collections import Counter


class SwordRecipe(Recipe):
    def __init__(self, visibleSprites: CameraSpriteGroup, loadedImages: LoadedImages):
        Recipe.__init__(self, visibleSprites, loadedImages)
        self.image.blit(loadedImages.sword, (0, 0))
        self.requiredItems = [Wood, SharpRock, SharpRock]
        self.itemToCraft = Sword

        itemDict = Counter(item.__name__ for item in self.requiredItems)

        requirementsStr = ""
        for key, value in itemDict.items():
            requirementsStr += f"{value}x {key}, "
        requirementsStr = requirementsStr[:-2]

        self.cratablMessage = f"Craft Sword from: {requirementsStr}"
        self.uncratablMessage = f"Requires: {requirementsStr}"
