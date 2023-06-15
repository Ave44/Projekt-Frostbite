from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.LoadedImages import LoadedImages
from game.ui.crafting.recipes.domain.Recipe import Recipe
from game.items.WoodenArmor import WoodenArmor
from game.items.Wood import Wood
from collections import Counter


class WoodenArmorRecipe(Recipe):
    def __init__(self, visibleSprites: CameraSpriteGroup, loadedImages: LoadedImages):
        Recipe.__init__(self, visibleSprites, loadedImages)
        self.image.blit(loadedImages.woodenArmor, (0, 0))
        self.requiredItems = [Wood, Wood, Wood, Wood, Wood, Wood]
        self.itemToCraft = WoodenArmor

        itemDict = Counter(item.__name__ for item in self.requiredItems)

        requirementsStr = ""
        for key, value in itemDict.items():
            requirementsStr += f"{value}x {key}, " 
        requirementsStr = requirementsStr[:-2]

        self.cratablMessage = f"Craft Wooden Armor from: {requirementsStr}"
        self.uncratablMessage = f"Requires: {requirementsStr}"
