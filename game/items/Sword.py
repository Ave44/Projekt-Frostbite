from game.LoadedImages import LoadedImages

from pygame.math import Vector2
from game.items.domain.Item import Item
from game.items.domain.Tool import Tool
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class Sword(Item, Tool):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages):
        name = "Sword"
        img = loadedImages.sword
        icon = loadedImages.sword

        Item.__init__(self, visibleSprites, center, loadedImages, name, img, icon)
        Tool.__init__(self, 10, 100)
