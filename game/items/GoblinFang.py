from pygame import Vector2
from game.LoadedImages import LoadedImages

from game.items.domain.Item import Item
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class GoblinFang(Item):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages, id: str = None):
        name = "Goblin Fang"
        img = loadedImages.goblinFang
        icon = loadedImages.goblinFang
        Item.__init__(self, visibleSprites, center, loadedImages, name, img, icon, id)
