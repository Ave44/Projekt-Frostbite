from game.LoadedImages import LoadedImages

from pygame.math import Vector2
from game.items.domain.Pickaxe import Pickaxe
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class StonePickaxe(Pickaxe):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages, currDurability: int = None, id: str = None):
        name = "Stone Pickaxe"
        image = loadedImages.stonePickaxe
        icon = loadedImages.stonePickaxe
        damage = 5
        durability = 100

        Pickaxe.__init__(self, visibleSprites, center, loadedImages, damage, durability, name, image, icon, id, currDurability)
