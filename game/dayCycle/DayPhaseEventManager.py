from typing import Callable

from game.dayCycle.domain.DayPhase import DayPhase
from game.dayCycle.domain.DayPhaseListener import DayPhaseListener


class DayPhaseEventManager:
    def __init__(self):
        self.listeners: dict[DayPhase, list[DayPhaseListener]] = {}
        self.dayPhasesNotifiers: dict[DayPhase, Callable[[DayPhaseListener], None]] = {
            DayPhase.DAY: (lambda listener: listener.onDay()),
            DayPhase.NIGHT: (lambda listener: listener.onNight()),
            DayPhase.MORNING: (lambda listener: listener.onMorning()),
            DayPhase.EVENING: (lambda listener: listener.onEvening())
        }

    def subscribe(self, dayPhaseEvent: DayPhase, listener: DayPhaseListener):
        eventListeners = self.listeners.get(dayPhaseEvent, [])
        eventListeners.append(listener)
        self.listeners[dayPhaseEvent] = eventListeners

    def unsubscribe(self, dayPhaseEvent: DayPhase, listener: DayPhaseListener):
        self.listeners[dayPhaseEvent].remove(listener)

    def notify(self, dayPhaseEvent: DayPhase):
        for listener in self.listeners.get(dayPhaseEvent, []):
            self.dayPhasesNotifiers[dayPhaseEvent](listener)
