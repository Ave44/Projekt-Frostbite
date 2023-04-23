from Config import Config
from constants import ATUMN_COLORS, WINTER_COLORS, SPRING_COLORS, SUMMER_COLORS
from pygame.time import Clock
from pygame import Surface, SRCALPHA

from game.ui.DayNightClock import DayNightClock
from game.Season import Season
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup


class DayCycle:
    def __init__(self, currentDay: int, currentTimeMs: int, dayLengthMs: int, clock: Clock,
                 config: Config, uiSprites: UiSpriteGroup, visibleSprites: CameraSpriteGroup):
        self.uiSprites = uiSprites

        self.clock = clock
        self.currentDay = currentDay
        self.currentTimeMs = currentTimeMs
        self.dayLengthMs = dayLengthMs
        self.daySegments = 24
        self.daySegmentLengthMs = dayLengthMs / self.daySegments

        atumn = Season([22, 20], [7, 9], 4, 4, 20, 20, ATUMN_COLORS)
        winter = Season([20, 18], [9, 11], 5, 5, 20, 10, WINTER_COLORS)
        spring = Season([20, 22], [9, 7], 4, 4, 20, 20, SPRING_COLORS)
        summer = Season([22, 24], [7, 5], 3, 3, 20, 10, SUMMER_COLORS)
        self.seasons = [atumn, winter, spring, summer]
        self.yearLength = sum(season.length for season in self.seasons)

        self.dayCycleClock = DayNightClock(self.dayLengthMs, self.daySegments, self.currentTimeMs, currentDay, 201)
        uiSprites.setClock(self.dayCycleClock)
        self.setDay(currentDay)

        self.nightMask = Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), SRCALPHA)
        self.updateNightMask()
        visibleSprites.nightMask = self.nightMask

    def updateDayCycle(self):
        deltaTime = self.clock.get_time()
        self.currentTimeMs = self.currentTimeMs + deltaTime
        if self.currentTimeMs >= self.dayLengthMs:
            self.currentTimeMs = 0
            self.setDay(self.currentDay + 1)

        self.updateNightMask()
        self.dayCycleClock.update(self.currentTimeMs)


    def updateNightMask(self) -> int:
        if self.currentTimeMs < self.dawnStart:
            brightness = 0
        elif self.currentTimeMs < self.dayStart:
            brightness = (self.currentTimeMs - self.dawnStart) / self.dawnLength * 255
        elif self.currentTimeMs < self.duskStart:
            brightness = 255
        elif self.currentTimeMs < self.nightStart:
            brightness = 255 - (self.currentTimeMs - self.duskStart) / self.duskLength * 255
        else:
            brightness = 0

        self.nightMask.fill((brightness, brightness, brightness))
    
    def setDay(self, day: int):
        self.currentDay = day
        self.dayCycleClock.currentDay = day

        seasonDay = self.currentDay % self.yearLength
        for season in self.seasons:
            seasonEnd = season.length
            if seasonEnd <= seasonDay:
                seasonDay -= seasonEnd
                continue
            dayPhases = season.getDayPhases(seasonDay, self.daySegmentLengthMs)
            break

        self.dawnStart = dayPhases[0]['start']
        self.dayStart = dayPhases[1]['start']
        self.duskStart = dayPhases[2]['start']
        self.nightStart = dayPhases[3]['start']

        self.dawnLength = self.dayStart - self.dawnStart
        self.duskLength = self.nightStart - self.duskStart

        self.dayCycleClock.updateBackground(dayPhases)
