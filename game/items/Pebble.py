from pygame import Vector2
from game.LoadedImages import LoadedImages

from game.items.domain.Item import Item
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class Pebble(Item):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages):
        name = "Pebble"
        img = loadedImages.pebble
        icon = loadedImages.pebble
        Item.__init__(self, visibleSprites, center, loadedImages, name, img, icon)
