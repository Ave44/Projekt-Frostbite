from abc import ABC, abstractmethod

from pygame import Vector2, Surface
from pygame.sprite import Group
from pygame.time import Clock

from game.items.ToolType import ToolType
from game.objects.domain.Object import Object


class Flammable(Object, ABC):
    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, bottomCenter: Vector2(), durability: int,
                 toolType: ToolType, image: Surface, clock: Clock, isOnFire: bool = False,
                 timeToBurnMs: int = 0, timeOnFireMs: int = 0):
        super().__init__(visibleGroup, obstaclesGroup, bottomCenter, durability, toolType, image)
        self.isOnFire = isOnFire
        self.timeToBurn = timeToBurnMs
        self.timeOnFire = timeOnFireMs
        self.clock = clock

    @abstractmethod
    def burn(self):
        pass

    def setOnFire(self, timeToBurnMs: int) -> None:
        self.isOnFire = True
        self.timeToBurn = timeToBurnMs

    def stopFire(self) -> None:
        self.isOnFire = False
        self.timeToBurn = 0

    def update(self) -> None:
        if not self.isOnFire or not self.timeToBurn:
            return
        self.timeOnFire += self.clock.get_time()
        if self.timeOnFire >= self.timeToBurn:
            self.burn()
