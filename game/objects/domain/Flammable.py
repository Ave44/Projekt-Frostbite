from abc import ABC, abstractmethod

from pygame import Vector2, Surface
from pygame.sprite import Group
from pygame.time import Clock

from game.items.ToolType import ToolType
from game.objects.domain.Object import Object


class Flammable(Object, ABC):
    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, bottomCenter: Vector2(), durability: int,
                 toolType: ToolType, image: Surface, clock: Clock):
        super().__init__(visibleGroup, obstaclesGroup, bottomCenter, durability, toolType, image)
        self.isOnFire = False
        self.timeLeft = 0
        self.damagePerAction = 0
        self.timeFromLastTick = 0
        self.clock = clock

    @abstractmethod
    def localUpdate(self):
        pass

    def burn(self, durationMs: int, damagePerAction: int) -> None:
        self.isOnFire = True
        self.timeLeft = durationMs
        self.damagePerAction = damagePerAction

    def update(self) -> None:
        self.localUpdate()

        if not self.isOnFire:
            return
        dt = self.clock.get_time()
        self.timeFromLastTick += dt
        self.timeLeft -= dt
        if self.timeFromLastTick > 1000:
            self.getDamage(self.damagePerAction)
            self.timeFromLastTick = 0
