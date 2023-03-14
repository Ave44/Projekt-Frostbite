import pygame
from pygame import Vector2
from pygame.sprite import Group
from pygame.time import Clock

from config import ROOT_PATH
from game.items.Sword import Sword
from game.items.ToolType import ToolType
from game.objects.domain.Flammable import Flammable


class Snag(Flammable):
    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, bottomCenter: Vector2, clock: Clock):
        image = pygame.image.load(f"{ROOT_PATH}/graphics/objects/tree/snag.png")
        super().__init__(visibleGroup, obstaclesGroup, bottomCenter, 1, ToolType.AXE, image, clock)

    def interact(self) -> None:
        print("interacted with snag")  # in the future there will be a real implementation

    def drop(self) -> None:
        Sword(self.visibleGroup, self.rect.center)  # in the future there will be a real implementation

    def localUpdate(self):
        pass
