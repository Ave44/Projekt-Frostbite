from abc import ABC, abstractmethod

from pygame.time import Clock


class Effect(ABC):
    from game.entities import Entity

    def __init__(self, durationMs: int, timeBetweenActionsMs: int, target: Entity, clock: Clock):
        self.timeLeft = durationMs
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
        dt = self.clock.get_time()
        self.timeFromLastTick += dt
        self.timeLeft -= dt
        if self.timeLeft <= 0:
            self.target.activeEffects.remove(self)
        elif self.canApply() and self.timeFromLastTick >= self.timeBetweenActions:
            self.action()
            self.timeFromLastTick = 0
