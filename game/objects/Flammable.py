from abc import ABC, abstractmethod

from pygame import Vector2, Surface
from pygame.sprite import Group
from pygame.time import Clock

from game.items.ToolType import ToolType
from game.objects.Object import Object


class Flammable(Object, ABC):
    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, bottomCenter: Vector2(), durability: int,
                 toolType: ToolType, image: Surface, clock: Clock):
        super().__init__(visibleGroup, obstaclesGroup, bottomCenter, durability, toolType, image)
        self.isOnFire = False
        self.timeLeft = 0
        self.damagePerTick = 0
        self.timeFromLastTick = 0
        self.clock = clock

    @abstractmethod
    def localUpdate(self):
        pass

    def burn(self, duration: int, damagePerTick: int) -> None:
        self.timeLeft = duration
        self.damagePerTick = damagePerTick

    def update(self) -> None:
        self.localUpdate()

        if not self.isOnFire:
            return
        dt = self.clock.get_time()
        self.timeFromLastTick += dt
        self.timeLeft -= dt
        if self.timeFromLastTick > 1000:
            self.getDamage(self.damagePerTick)
            self.timeFromLastTick = 0
