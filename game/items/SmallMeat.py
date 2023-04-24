from pygame import Vector2
from game.LoadedImages import LoadedImages

from game.entities.Player import Player
from game.items.domain.Item import Item
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class SmallMeat(Item):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages):
        name = "Small Meat"
        img = loadedImages.smallMeat
        icon = loadedImages.smallMeat
        Item.__init__(self, visibleSprites, center, loadedImages, name, img, icon)

    def use(self, player: Player):
        player.heal(20)
