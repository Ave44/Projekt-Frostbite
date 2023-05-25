from Config import Config
from constants import DAY_LENGTH_MS
from pygame.time import Clock

from game.dayCycle.domain.DayPhase import DayPhase
from game.dayCycle.DayPhaseEventManager import DayPhaseEventManager
from game.dayCycle.season.SeasonController import SeasonController
from game.ui.DayNightClock import DayNightClock
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup



class DayCycle:
    def __init__(self, currentDay: int, currentTimeMs: int, clock: Clock,
                 config: Config, uiSprites: UiSpriteGroup, visibleSprites: CameraSpriteGroup):
        self.uiSprites = uiSprites
        self.visibleSprites = visibleSprites

        self.clock = clock
        self.currentDay = currentDay
        self.currentTimeMs = currentTimeMs
        self.dayLengthMs = DAY_LENGTH_MS
        self.seasonController = SeasonController()

        self.events = DayPhaseEventManager()

        self.dayCycleClock = DayNightClock(self.dayLengthMs, self.currentTimeMs, currentDay, 201, config.font)
        uiSprites.setClock(self.dayCycleClock)
        self.setDay(currentDay)

        brightness, self.currentDayPhase = self.calculateDayPhase()
        self.visibleSprites.updateNightMask(brightness)

    def update(self):
        deltaTime = self.clock.get_time()
        self.currentTimeMs = self.currentTimeMs + deltaTime
        if self.currentTimeMs >= self.dayLengthMs:
            self.currentTimeMs = 0
            self.setDay(self.currentDay + 1)

        brightness, phase = self.calculateDayPhase()

        if self.currentDayPhase != phase:
            self.events.notify(phase)
            self.currentDayPhase = phase

        self.visibleSprites.updateNightMask(brightness)

        self.dayCycleClock.update(self.currentTimeMs)

    def calculateDayPhase(self) -> tuple[int, DayPhase]:
        if self.currentTimeMs < self.dawnStart:
            brightness = 0
            dayPhase = DayPhase.NIGHT
        elif self.currentTimeMs < self.dayStart:
            brightness = (self.currentTimeMs - self.dawnStart) / self.dawnLength * 255
            dayPhase = DayPhase.MORNING
        elif self.currentTimeMs < self.duskStart:
            brightness = 255
            dayPhase = DayPhase.DAY
        elif self.currentTimeMs < self.nightStart:
            brightness = 255 - (self.currentTimeMs - self.duskStart) / self.duskLength * 255
            dayPhase = DayPhase.EVENING
        else:
            brightness = 0
            dayPhase = DayPhase.NIGHT

        return brightness, dayPhase

    def setDay(self, day: int):
        self.currentDay = day
        self.dayCycleClock.currentDay = day

        dayPhasesStartTimeWithColors = self.seasonController.getDayPhasesOfCurrentSeason(self.currentDay)
        self.dayCycleClock.updateBackground(dayPhasesStartTimeWithColors)

        dayPhasesStartTime = [dayPhaseWithColor[0] for dayPhaseWithColor in dayPhasesStartTimeWithColors]
        self.dawnStart = dayPhasesStartTime[0]
        self.dayStart = dayPhasesStartTime[1]
        self.duskStart = dayPhasesStartTime[2]
        self.nightStart = dayPhasesStartTime[3]

        self.dawnLength = self.dayStart - self.dawnStart
        self.duskLength = self.nightStart - self.duskStart


    def isNight(self) -> bool:
        if self.currentTimeMs > self.nightStart or self.currentTimeMs < self.dawnStart:
            return True
        return False

    def skipNight(self):
        if self.currentTimeMs > self.nightStart:
            self.currentTimeMs = self.dawnStart
            self.setDay(self.currentDay + 1)
        elif self.currentTimeMs < self.dawnStart:
            self.currentTimeMs = self.dawnStart
        self.update()
