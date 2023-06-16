from game.LoadedImages import LoadedImages

from pygame.math import Vector2
from game.items.domain.Tool import Tool
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class Mace(Tool):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages, currDurability: int = None, id: str = None):
        name = "Mace"
        image = loadedImages.mace
        icon = loadedImages.mace
        damage = 20
        durability = 100

        Tool.__init__(self, visibleSprites, center, loadedImages, damage, durability, name, image, icon, id, currDurability)
