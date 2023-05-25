from abc import ABC,abstractmethod

from game.dayCycle.domain.DayPhase import DayPhase


class DayPhaseListener(ABC):
    @abstractmethod
    def onDayPhaseChange(self, dayPhase: DayPhase):
        pass