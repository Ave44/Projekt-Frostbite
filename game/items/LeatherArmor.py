from pygame import Vector2
from game.LoadedImages import LoadedImages

from game.items.domain.Item import Item
from game.items.domain.Armor import Armor
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class LeatherArmor(Item, Armor):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages):
        name = "LeatherArmor"
        img = loadedImages.leatherArmor
        icon = loadedImages.leatherArmor
        Item.__init__(self, visibleSprites, center, loadedImages, name, img, icon)
        Armor.__init__(self, gainedDamageModifier=0.6)
