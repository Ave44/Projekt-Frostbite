from game.LoadedImages import LoadedImages

from pygame.math import Vector2
from game.items.domain.Axe import Axe
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class StoneAxe(Axe):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages, currDurability: int = None, id: str = None):
        name = "StoneAxe"
        image = loadedImages.stoneAxe
        icon = loadedImages.stoneAxe
        damage = 5
        durability = 100

        Axe.__init__(self, visibleSprites, center, loadedImages, damage, durability, name, image, icon, id, currDurability)
