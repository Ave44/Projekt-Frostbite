from pygame import Vector2
from game.LoadedImages import LoadedImages

from game.items.domain.Item import Item
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class BoarFang(Item):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages):
        name = "Boar Fang"
        img = loadedImages.boarFang
        icon = loadedImages.boarFang
        Item.__init__(self, visibleSprites, center, name, img, icon)
