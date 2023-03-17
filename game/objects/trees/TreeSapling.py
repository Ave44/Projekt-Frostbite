import pygame
from pygame import Vector2, Rect
from pygame.sprite import Group
from pygame.time import Clock

from config import ROOT_PATH
from game.items.Item import Item
from game.items.ToolType import ToolType
from game.objects.domain.CollisionObject import CollisionObject
from game.objects.domain.Object import Object
from game.objects.trees.SmallTree import SmallTree


class TreeSapling(CollisionObject):
    _LIFESPAN = 36000

    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, midBottom: Vector2, clock: Clock):
        image = pygame.image.load(f"{ROOT_PATH}/graphics/objects/trees/sapling.png")
        hitBox = Rect((0, 0), (5, 5))
        hitBox.midbottom = midBottom
        super().__init__(visibleGroup, obstaclesGroup, midBottom, 1, ToolType.HAND, image, hitBox)

        self.clock = clock
        self.age = 0

    def interact(self) -> None:
        print("interacted with sapling")  # in the future there will be a real implementation

    def drop(self) -> None:
        Item(self.visibleGroup, self.rect.center)

    def update(self) -> None:
        self.age += self.clock.get_time()
        if self.age >= self._LIFESPAN:
            self.remove(*self.groups())
            SmallTree(self.visibleGroup, self.obstaclesGroup, self.rect.midbottom, self.clock)
