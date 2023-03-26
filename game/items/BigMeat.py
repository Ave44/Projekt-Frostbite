from pygame import Vector2, image

from config import ROOT_PATH
from game.items.domain.Item import Item
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class BigMeat(Item):
    def __init__(self, visibleSpritesGroup: CameraSpriteGroup, center: Vector2):
        name = "Big Meat"
        img = image.load(f"{ROOT_PATH}/graphics/items/big_meat.png")
        icon = image.load(f"{ROOT_PATH}/graphics/items/big_meat.png")
        super().__init__(visibleSpritesGroup, center, name, img, icon)

    def use(self):
        print(self, "was used")
