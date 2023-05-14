from game.LoadedImages import LoadedImages

from pygame.math import Vector2
from game.items.domain.Tool import Tool
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class Sword(Tool):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages, currDurability: int = None, id: str = None):
        name = "Sword"
        image = loadedImages.sword
        icon = loadedImages.sword
        damage = 10
        durability = 100

        Tool.__init__(self, visibleSprites, center, loadedImages, damage, durability, name, image, icon, id, currDurability)
