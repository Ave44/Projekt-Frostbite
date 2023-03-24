from pygame import Vector2, image

from config import ROOT_PATH
from game.items.Item import Item
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class BigMeat(Item):
    def __init__(self, visibleSpritesGroup: CameraSpriteGroup, center: Vector2):
        super().__init__(visibleSpritesGroup, center)
        self.name = "Big Meat"
        self.image = image.load(f"{ROOT_PATH}/graphics/items/big_meat.png")
        self.icon = image.load(f"{ROOT_PATH}/graphics/items/big_meat.png")

    def use(self):
        print(self, "was used")
