import pygame
from pygame.math import Vector2
from pygame.sprite import Group
from pygame.time import Clock

from config import ROOT_PATH
from game.items.Sword import Sword
from game.items.ToolType import ToolType
from game.objects.Object import Object


class Grass(Object):
    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, center: Vector2(),
                 clock: Clock):
        normalImage = pygame.image.load(f"{ROOT_PATH}/graphics/objects/grass.png")
        super().__init__(visibleGroup, obstaclesGroup,
                         center, 1, ToolType.SHOVEL,
                         True, clock, normalImage,
                         normalImage, normalImage)

    def dropItem(self) -> None:
        Sword(self.visibleGroup, self.rect.center)
