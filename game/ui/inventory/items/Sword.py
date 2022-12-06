from config import ROOT_PATH
from ui.inventory.items.Item import Item
import pygame


class Sword(Item):
    def __init__(self, groups: pygame.sprite.Group, center: pygame.math.Vector2()):
        super().__init__(groups, center)
        self.name = "Sword"
        self.image = pygame.image.load(f"{ROOT_PATH}/graphics/items/sword.png")
        self.icon = pygame.image.load(f"{ROOT_PATH}/graphics/items/sword.png")
        self.damage = 10
        self.durability = 100

    def use(self):
        print(self, "was used")
