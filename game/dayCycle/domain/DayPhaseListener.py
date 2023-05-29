from abc import ABC,abstractmethod

from game.dayCycle.domain.DayPhase import DayPhase


class DayPhaseListener:
    def onDay(self):
        pass

    def onEvening(self):
        pass

    def onMorning(self):
        pass

    def onNight(self):
        pass