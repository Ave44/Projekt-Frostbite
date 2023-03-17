import pygame
from pygame import Vector2, Rect
from pygame.sprite import Group
from pygame.time import Clock

from config import ROOT_PATH
from game.items.Item import Item
from game.items.ToolType import ToolType
from game.objects.domain.CollisionObject import CollisionObject
from game.objects.domain.Flammable import Flammable
from game.objects.trees.BurntTree import BurntTree
from game.objects.trees.LargeTree import LargeTree


class MediumTree(CollisionObject, Flammable):
    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, midBottom: Vector2, clock: Clock, ageMs: int = 0):
        image = pygame.image.load(f"{ROOT_PATH}/graphics/objects/trees/mediumTree.png")
        coliderRect = Rect((0, 0), (5, 5))
        coliderRect.midbottom = midBottom

        CollisionObject.__init__(self, visibleGroup, obstaclesGroup, midBottom, 10, ToolType.AXE, image, coliderRect)
        Flammable.__init__(self, clock)

        self.age = ageMs
        self.LIFESPAN = 10000

    def interact(self) -> None:
        print("interacted with medium trees")  # in the future there will be a real implementation

    def drop(self) -> None:
        Item(self.visibleGroup, self.rect.center)  # in the future there will be a real implementation

    def burn(self):
        self.remove(*self.groups())
        BurntTree(self.visibleGroup, self.obstaclesGroup, self.rect.midbottom)

    def update(self):
        if self.isOnFire and self.timeToBurn:
            self.flameUpdate()
            return
        self.age += self.clock.get_time()
        if self.age >= self.LIFESPAN:
            self.remove(*self.groups())
            LargeTree(self.visibleGroup, self.obstaclesGroup, self.rect.midbottom, self.clock)
