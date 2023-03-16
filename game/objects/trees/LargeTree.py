import pygame
from pygame.math import Vector2
from pygame.sprite import Group
from pygame.time import Clock

from config import ROOT_PATH
from game.items.Item import Item
from game.items.ToolType import ToolType
from game.objects.domain.Flammable import Flammable
from game.objects.trees.BurntTree import BurntTree
from game.objects.trees.Snag import Snag


class LargeTree(Flammable):
    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, bottomCenter: Vector2(),
                 clock: Clock, ageMs: int = 0):
        image = pygame.image.load(f"{ROOT_PATH}/graphics/objects/trees/largeTree.png")
        super().__init__(visibleGroup, obstaclesGroup,
                         bottomCenter, 10, ToolType.AXE, image, clock)
        self.age = ageMs
        self.LIFESPAN = 10000

    def interact(self) -> None:
        print("interacted with medium trees")  # in the future there will be a real implementation

    def drop(self) -> None:
        Item(self.visibleGroup, self.rect.center)  # in the future there will be a real implementation

    def burn(self):
        self.visibleGroup.remove(self)
        self.obstaclesGroup.remove(self)
        BurntTree(self.visibleGroup, self.obstaclesGroup, self.rect.midbottom)

    def localUpdate(self):
        if self.isOnFire:
            return
        self.age += self.clock.get_time()
        if self.age >= self.LIFESPAN:
            self.visibleGroup.remove(self)
            self.obstaclesGroup.remove(self)
            Snag(self.visibleGroup, self.obstaclesGroup, self.rect.midbottom, self.clock)
