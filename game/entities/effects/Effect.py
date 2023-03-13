from abc import ABC, abstractmethod

from pygame.time import Clock


class Effect(ABC):
    from game.entities import Entity

    def __init__(self, durationMiliSeconds: int, timeBetweenActionsMs: int, target: Entity, clock: Clock):
        self.timeLeft = durationMiliSeconds
        self.target = target
        self.clock = clock
        self.timeFromLastTick = 0
        self.timeBetweenActions = timeBetweenActionsMs

    @abstractmethod
    def canApply(self) -> bool:
        pass

    @abstractmethod
    def action(self) -> None:
        pass

    def execute(self) -> None:
        if self.canApply() and self.timeLeft:
            dt = self.clock.get_time()
            self.timeFromLastTick += dt
            self.timeLeft -= dt
            if self.timeFromLastTick >= self.timeBetweenActions:
                self.action()
                self.timeFromLastTick = 0
