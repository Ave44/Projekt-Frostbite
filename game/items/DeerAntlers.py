from pygame import Vector2
from game.LoadedImages import LoadedImages

from game.items.domain.Item import Item
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class DeerAntlers(Item):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages, id: str = None):
        name = "Deer Antlers"
        img = loadedImages.deerAntlers
        icon = loadedImages.deerAntlers
        Item.__init__(self, visibleSprites, center, loadedImages, name, img, icon, id)
