import pygame

from config import ROOT_PATH
from pygame.math import Vector2
from game.items.Item import Item


class Sword(Item):
    def __init__(self, groups: pygame.sprite.Group, center: Vector2()):
        super().__init__(groups, center)
        self.name = "Sword"
        self.image = pygame.image.load(f"{ROOT_PATH}/graphics/items/sword.png").convert_alpha()
        self.icon = pygame.image.load(f"{ROOT_PATH}/graphics/items/sword.png").convert_alpha()
        self.damage = 10
        self.durability = 100

    def use(self):
        print(self, "was used")
