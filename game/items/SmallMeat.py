from pygame import Vector2, image

from config import ROOT_PATH
from game.items.domain.Item import Item
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class SmallMeat(Item):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2):
        name = "Small Meat"
        img = image.load(f"{ROOT_PATH}/graphics/items/small_meat.png")
        icon = image.load(f"{ROOT_PATH}/graphics/items/small_meat.png")
        super().__init__(visibleSprites, center, name, img, icon)
