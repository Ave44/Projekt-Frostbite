from game.LoadedImages import LoadedImages

from pygame.math import Vector2
from game.items.domain.Item import Item
from game.items.domain.Axe import Axe
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class StoneAxe(Item, Axe):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages):
        name = "StoneAxe"
        img = loadedImages.stoneAxe
        icon = loadedImages.stoneAxe

        Item.__init__(self, visibleSprites, center, loadedImages, name, img, icon)
        Axe.__init__(self, 5, 100)
