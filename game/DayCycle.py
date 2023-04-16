from Config import Config
from constants import DAWN_COLOR, DAY_COLOR, DUSK_COLOR, NIGHT_COLOR
from pygame.time import Clock
from pygame import Surface, SRCALPHA

from game.DayNightClock import DayNightClock
from game.Season import Season
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup


class DayCycle:
    def __init__(self, currentDay: int, currentTimeMs: int, dayLengthMs: int, clock: Clock,
                 config: Config, uiSprites: UiSpriteGroup, visibleSprites: CameraSpriteGroup):
        self.uiSprites = uiSprites

        self.clock = clock
        self.currentDay = currentDay
        self.currentTimeMS = currentTimeMs
        self.dayLengthMs = dayLengthMs
        self.daySegments = 24
        self.daySegmentLengthMs = dayLengthMs / self.daySegments

        self.nightMask = Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), SRCALPHA)
        self.nightMask.fill((255, 255, 255))

        self.yearLength = 40
        self.atumn = Season([5, 3], [8, 6], [18, 20], [21, 23], 20)

        self.dawnStart = 6 * self.daySegmentLengthMs
        self.dayStart = 8 * self.daySegmentLengthMs
        self.duskStart = 20 * self.daySegmentLengthMs
        self.nightStart = 22 * self.daySegmentLengthMs

        self.dawnLength = self.dayStart - self.dawnStart
        self.duskLength = self.nightStart - self.duskStart

        visibleSprites.sunlight = self.nightMask

        dayPhases = [
            (self.dawnStart, NIGHT_COLOR),
            (self.dawnLength, DAWN_COLOR),
            (self.duskStart - self.dayStart, DAY_COLOR),
            (self.duskLength, DUSK_COLOR),
            (dayLengthMs - self.nightStart, NIGHT_COLOR)
        ]
        self.dayCycleClock = DayNightClock(dayPhases, self.daySegments, self.currentTimeMS, currentDay, 201)
        uiSprites.setClock(self.dayCycleClock)

    def updateDayCycle(self):
        deltaTime = self.clock.get_time()
        self.currentTimeMS = self.currentTimeMS + deltaTime
        if self.currentTimeMS >= self.dayLengthMs:
            self.currentTimeMS = 0
            self.setDay(self.currentDay + 1)

        brightness = self.calculateBrightness()
        self.nightMask.fill((brightness, brightness, brightness))
        self.dayCycleClock.update(self.currentTimeMS)


    def calculateBrightness(self) -> int:
        if self.currentTimeMS < self.dawnStart:
            brightness = 0
        elif self.currentTimeMS < self.dayStart:
            brightness = (self.currentTimeMS - self.dawnStart) / self.dawnLength * 255
        elif self.currentTimeMS < self.duskStart:
            brightness = 255
        elif self.currentTimeMS < self.nightStart:
            brightness = 255 - (self.currentTimeMS - self.duskStart) / self.duskLength * 255
        else:
            brightness = 0
        return brightness
    
    def setDay(self, day: int):
        self.currentDay = day
        self.dayCycleClock.currentDay = day
        yearDay = self.currentDay % self.yearLength
        seasonDay = yearDay % self.atumn.length

        dayPhases = self.atumn.getDayPhases(seasonDay)

        self.dawnStart = dayPhases[0] * self.daySegmentLengthMs
        self.dayStart = dayPhases[1] * self.daySegmentLengthMs
        self.duskStart = dayPhases[2] * self.daySegmentLengthMs
        self.nightStart = dayPhases[3] * self.daySegmentLengthMs

        self.changeDayPhases(1)

    def changeDayPhases(self, newDayPhases: list[int]):
        # self.dawnStart = newDayPhases[0] * self.daySegmentLengthMs
        # self.dayStart = newDayPhases[1] * self.daySegmentLengthMs
        # self.duskStart = newDayPhases[2] * self.daySegmentLengthMs
        # self.nightStart = newDayPhases[3] * self.daySegmentLengthMs

        self.dawnLength = self.dayStart - self.dawnStart
        self.duskLength = self.nightStart - self.duskStart

        dayPhases = [
            (self.dawnStart, NIGHT_COLOR),
            (self.dawnLength, DAWN_COLOR),
            (self.duskStart - self.dayStart, DAY_COLOR),
            (self.duskLength, DUSK_COLOR),
            (self.dayLengthMs - self.nightStart, NIGHT_COLOR)
        ]
        self.dayCycleClock.updateBackground(dayPhases)
