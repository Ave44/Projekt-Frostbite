from pygame import Surface

from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.LoadedImages import LoadedImages
from game.ui.crafting.Recipe import Recipe
from game.items.domain.Item import Item
from game.items.Wood import Wood
from game.items.SharpRock import SharpRock
from game.items.Pebble import Pebble
from game.items.Leather import Leather
from game.items.DeerAntlers import DeerAntlers
from game.items.BoarFang import BoarFang
from game.items.GoblinFang import GoblinFang
from game.items.GrassFibers import GrassFibers
from game.items.LeatherArmor import LeatherArmor
from game.items.Sword import Sword
from game.items.Mace import Mace
from game.items.StoneAxe import StoneAxe
from game.items.StonePickaxe import StonePickaxe
from game.items.GoblinPickaxe import GoblinPickaxe
from game.items.WoodenArmor import WoodenArmor
from game.items.LeatherArmor import LeatherArmor

class recipeListCreator:
    def __init__(self, visibleSprites: CameraSpriteGroup, loadedImages: LoadedImages) -> None:
        self.visibleSprites = visibleSprites
        self.loadedImages = loadedImages
        self.recipesList = []
        self.addRecipe(Sword, [Wood, SharpRock, SharpRock], loadedImages.sword)
        self.addRecipe(Mace, [Wood, Wood, BoarFang, BoarFang], loadedImages.mace)
        self.addRecipe(StoneAxe, [Wood, SharpRock], loadedImages.stoneAxe)
        self.addRecipe(StonePickaxe, [Wood, Pebble, SharpRock], loadedImages.stonePickaxe)
        self.addRecipe(GoblinPickaxe, [DeerAntlers, GoblinFang, GoblinFang, GrassFibers, GrassFibers], loadedImages.goblinPickaxe)
        self.addRecipe(WoodenArmor, [Wood, Wood, Wood, Wood, GrassFibers, GrassFibers], loadedImages.woodenArmor)
        self.addRecipe(LeatherArmor, [Leather, Leather, GrassFibers], loadedImages.leatherArmor)

    def addRecipe(self, itemToCraft: Item, requiredItems: list[Item], craftImage: Surface) -> None:
        recipe = Recipe(self.visibleSprites, self.loadedImages, itemToCraft, requiredItems, craftImage)
        self.recipesList.append(recipe)
