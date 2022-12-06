import pygame
from pygame.math import Vector2
from config import ROOT_PATH
from game.items.Item import Item

class Sword(Item):
    def __init__(self, groups: list[pygame.sprite.Group], center: Vector2()):
        super().__init__(groups, center)
        self.name = "Sword"
        self.image = pygame.image.load(f"{ROOT_PATH}/graphics/items/sword.png")
        self.icon = pygame.image.load(f"{ROOT_PATH}/graphics/items/sword.png")
        self.damage = 10
        self.durability = 100

    def use(self):
        print(self, "was used")