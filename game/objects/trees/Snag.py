import pygame
from pygame import Vector2
from pygame.sprite import Group
from pygame.time import Clock

from config import ROOT_PATH
from game.items.Item import Item
from game.items.ToolType import ToolType
from game.objects.domain.Flammable import Flammable
from game.objects.trees.BurntTree import BurntTree
from game.objects.trees.SmallTree import SmallTree


class Snag(Flammable):
    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, bottomCenter: Vector2, clock: Clock, age: int = 0):
        image = pygame.image.load(f"{ROOT_PATH}/graphics/objects/trees/snag.png")
        super().__init__(visibleGroup, obstaclesGroup, bottomCenter, 1, ToolType.AXE, image, clock)
        self.age = age
        self.LIFESPAN = 100000

    def interact(self) -> None:
        print("interacted with snag")  # in the future there will be a real implementation

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
            SmallTree(self.visibleGroup, self.obstaclesGroup, self.rect.midbottom, self.clock)
