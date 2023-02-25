from abc import ABC, abstractmethod

from pygame.time import Clock


class Effect(ABC):
    from game.objects import Object

    def __init__(self, amountOfTicks: int, object: Object, clock: Clock):
        self.amountOfTicks = amountOfTicks
        self.object = object
        self.clock = clock
        self.timeFromLastTick = clock.get_time()

    @abstractmethod
    def canApply(self) -> bool:
        pass

    @abstractmethod
    def action(self) -> None:
        pass

    def execute(self) -> None:
        if self.canApply() and self.amountOfTicks:
            self.timeFromLastTick += self.clock.get_time()
            if self.timeFromLastTick >= 1000:
                self.action()
                self.amountOfTicks -= 1
                self.timeFromLastTick = 0
