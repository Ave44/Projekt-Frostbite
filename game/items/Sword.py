from game.LoadedImages import LoadedImages

from pygame.math import Vector2
from game.items.domain.Item import Item
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class Sword(Item):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages):
        name = "Sword"
        image = loadedImages.sword
        icon = loadedImages.sword
        Item.__init__(self, visibleSprites, center, name, image, icon)
        self.damage = 10
        self.durability = 100

    def use(self):
        print(self, "was used")
