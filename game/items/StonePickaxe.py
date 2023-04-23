from game.LoadedImages import LoadedImages

from pygame.math import Vector2
from game.items.domain.Item import Item
from game.items.domain.Pickaxe import Pickaxe
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class StonePickaxe(Item, Pickaxe):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages):
        name = "StonePickaxe"
        img = loadedImages.stonePickaxe
        icon = loadedImages.stonePickaxe

        Item.__init__(self, visibleSprites, center, loadedImages, name, img, icon)
        Pickaxe.__init__(self, 5, 100)
