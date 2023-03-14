import pygame
from pygame.math import Vector2
from pygame.sprite import Group
from pygame.time import Clock

from config import ROOT_PATH
from game.items.Sword import Sword
from game.items.ToolType import ToolType
from game.objects.Flammable import Flammable


class Tree(Flammable):
    _LIFESPAN = 10000

    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, bottomCenter: Vector2(),
                 clock: Clock):
        image = pygame.image.load(f"{ROOT_PATH}/graphics/objects/tree/tree.png")
        super().__init__(visibleGroup, obstaclesGroup,
                         bottomCenter, 10, ToolType.AXE, image, clock)
        self.age = 0

    def interact(self) -> None:
        print("interacted with medium tree")  # in the future there will be a real implementation

    def dropItem(self) -> None:
        Sword(self.visibleGroup, self.rect.center)  # in the future there will be a real implementation

    def localUpdate(self):
        if self.isOnFire:
            return
        self.age += self.clock.get_time()
        if self.age >= self._LIFESPAN:
            self.visibleGroup.remove(self)
            self.obstaclesGroup.remove(self)
            Snag(self.visibleGroup, self.obstaclesGroup, self.rect.midbottom, self.clock)
