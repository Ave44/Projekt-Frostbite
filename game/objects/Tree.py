import pygame
from pygame.math import Vector2
from pygame.sprite import Group
from pygame.time import Clock

from config import ROOT_PATH
from game.items.Sword import Sword
from game.items.ToolType import ToolType
from game.objects.Flammable import Flammable


class Tree(Flammable):
    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, bottomCenter: Vector2(),
                 clock: Clock):
        image = pygame.image.load(f"{ROOT_PATH}/graphics/objects/tree/tree.png")
        super().__init__(visibleGroup, obstaclesGroup,
                         bottomCenter, 10, ToolType.AXE, image, clock)

    def localUpdate(self):
        pass

    def interact(self) -> None:
        # do something
        pass

    def dropItem(self) -> None:
        Sword(self.visibleGroup, self.rect.center)
