from pygame import Vector2
from game.LoadedImages import LoadedImages

from game.items.domain.Item import Item
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class GoblinChampionFibers(Item):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages):
        name = "GoblinChampion Fibers"
        img = loadedImages.grassFibers
        icon = loadedImages.grassFibers
        Item.__init__(self, visibleSprites, center, loadedImages, name, img, icon)
