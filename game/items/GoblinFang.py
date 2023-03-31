from pygame import Vector2, image

from config import ROOT_PATH
from game.items.domain.Item import Item
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class GoblinFang(Item):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2):
        name = "Goblin Fang"
        img = image.load(f"{ROOT_PATH}/graphics/items/goblin_fang.png").convert_alpha()
        icon = image.load(f"{ROOT_PATH}/graphics/items/goblin_fang.png").convert_alpha()
        super().__init__(visibleSprites, center, name, img, icon)
