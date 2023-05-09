from pygame import Vector2
from game.LoadedImages import LoadedImages

from game.items.domain.Item import Item
from game.entities.Player import Player
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class BigMeat(Item):
    def __init__(self, visibleSpritesGroup: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages):
        name = "Big Meat"
        img = loadedImages.bigMeat
        icon = loadedImages.bigMeat
        Item.__init__(self, visibleSpritesGroup, center, loadedImages, name, img, icon)

    def use(self, player: Player):
        player.heal(30)
        player.satiate(50)
