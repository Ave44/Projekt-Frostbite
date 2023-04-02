from pygame import Vector2
from game.LoadedImages import LoadedImages

from game.items.domain.Item import Item
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class Accorn(Item):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages):
        name = "Accorn"
        img = loadedImages.accorn
        icon = loadedImages.accorn
        Item.__init__(self, visibleSprites, center, loadedImages, name, img, icon)
