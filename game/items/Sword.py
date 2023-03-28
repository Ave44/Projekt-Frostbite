import pygame

from config import ROOT_PATH
from pygame.math import Vector2
from game.items.domain.Item import Item
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class Sword(Item):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2):
        name = "Sword"
        image = pygame.image.load(f"{ROOT_PATH}/graphics/items/sword.png").convert_alpha()
        icon = pygame.image.load(f"{ROOT_PATH}/graphics/items/sword.png").convert_alpha()
        super().__init__(visibleSprites, center, name, image, icon)
        self.damage = 10
        self.durability = 100

    def use(self):
        print(self, "was used")
