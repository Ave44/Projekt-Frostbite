from abc import ABC, abstractmethod

from pygame.time import Clock


class Effect(ABC):
    from game.entities import Entity

    def __init__(self, durationMiliSeconds: int, amountOfTicks: int, target: Entity, clock: Clock):
        self.timeLeft = durationMiliSeconds
        self.amountOfTicks = amountOfTicks
        self.target = target
        self.clock = clock
        self.timeFromLastTick = 0
        self.timeBetweenTicks = durationMiliSeconds / amountOfTicks

    @abstractmethod
    def canApply(self) -> bool:
        pass

    @abstractmethod
    def action(self) -> None:
        pass

    def execute(self) -> None:
        if self.canApply() and self.amountOfTicks:
            dt = self.clock.get_time()
            self.timeFromLastTick += dt
            self.timeLeft -= dt
            if self.timeFromLastTick >= self.timeBetweenTicks:
                self.action()
                self.amountOfTicks -= 1
                self.timeFromLastTick = 0
