import pygame
from pygame import Vector2
from pygame.sprite import Group
from pygame.time import Clock

from config import ROOT_PATH
from game.items.Sword import Sword
from game.items.ToolType import ToolType
from game.objects.Object import Object
from game.objects.SmallTree import SmallTree


class TreeSapling(Object):
    _LIFESPAN = 36000

    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, midBottom: Vector2, clock: Clock):
        image = pygame.image.load(f"{ROOT_PATH}/graphics/objects/sapling.png")
        super().__init__(visibleGroup, obstaclesGroup, midBottom, 1, ToolType.HAND, image)
        self.clock = clock
        self.age = 0

    def interact(self) -> None:
        print("interacted with sapling")  # in the future there will be a real implementation

    def dropItem(self) -> None:
        Sword(self.visibleGroup, self.rect.center)

    def update(self) -> None:
        self.age += self.clock.get_time()
        if self.age >= self._LIFESPAN:
            self.visibleGroup.remove(self)
            self.obstaclesGroup.remove(self)
            SmallTree(self.visibleGroup, self.obstaclesGroup, self.rect.midbottom, self.clock)
