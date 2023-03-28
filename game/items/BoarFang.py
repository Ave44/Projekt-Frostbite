from pygame import Vector2, image

from config import ROOT_PATH
from game.items.domain.Item import Item
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class BoarFang(Item):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2):
        name = "Boar Fang"
        img = image.load(f"{ROOT_PATH}/graphics/items/boar_fang.png")
        icon = image.load(f"{ROOT_PATH}/graphics/items/boar_fang.png")
        super().__init__(visibleSprites, center, name, img, icon)
