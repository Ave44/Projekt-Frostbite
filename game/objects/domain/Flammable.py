from abc import ABC, abstractmethod
from pygame.time import Clock

class Flammable(ABC):
    def __init__(self, clock: Clock, isOnFire: bool = False,
                 timeToBurnMs: int = 0, timeOnFireMs: int = 0):
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

    def flameUpdate(self) -> None:
        self.timeOnFire += self.clock.get_time()
        if self.timeOnFire >= self.timeToBurn:
            self.burn()
