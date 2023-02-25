import pygame
from pygame.math import Vector2
from pygame.sprite import Group
from pygame.time import Clock

from config import ROOT_PATH
from game.items.Sword import Sword
from game.items.ToolType import ToolType
from game.objects.Object import Object


class Tree(Object):
    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, center: Vector2(),
                 clock: Clock):
        imageNormal = pygame.image.load(f"{ROOT_PATH}/graphics/objects/tree/tree.png")
        imageDamage = pygame.image.load(f"{ROOT_PATH}/graphics/objects/tree/tree_damage.png")
        imageHeal = pygame.image.load(f"{ROOT_PATH}/graphics/objects/tree/tree_heal.png")
        super().__init__(visibleGroup, obstaclesGroup,
                         center, 10, ToolType.AXE,
                         True, clock, imageNormal,
                         imageDamage, imageHeal)

    def dropItem(self) -> None:
        Sword(self.visibleGroup, self.rect.center)
