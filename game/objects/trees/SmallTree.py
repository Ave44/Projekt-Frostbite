import pygame
from pygame import Vector2
from pygame.sprite import Group
from pygame.time import Clock

from config import ROOT_PATH
from game.items.ToolType import ToolType
from game.objects.trees.BurntTree import BurntTree
from game.objects.domain.Flammable import Flammable
from game.objects.trees.MediumTree import MediumTree


class SmallTree(Flammable):
    _LIFESPAN = 20000

    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, midBottom: Vector2, clock: Clock):
        image = pygame.image.load(f"{ROOT_PATH}/graphics/objects/trees/smallTree.png")
        super().__init__(visibleGroup, obstaclesGroup, midBottom, 5, ToolType.AXE, image, clock)
        self.age = 0

    def interact(self) -> None:
        print("interacted with small trees")  # in the future there will be a real implementation

    def drop(self) -> None:
        BurntTree(self.visibleGroup, self.obstaclesGroup, self.rect.midbottom)

    def localUpdate(self):
        if self.isOnFire:
            return
        self.age += self.clock.get_time()
        if self.age >= self._LIFESPAN:
            self.visibleGroup.remove(self)
            self.obstaclesGroup.remove(self)
            MediumTree(self.visibleGroup, self.obstaclesGroup, self.rect.midbottom, self.clock)
