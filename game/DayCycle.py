import pygame
from Config import Config
from pygame.time import Clock
from pygame import Surface, Color, SRCALPHA

from game.DayNightClock import DayNightClock
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup


class DayCycle:
    def __init__(self, currentTimeInMs: int, dayLengthInMs: int, clock: Clock, config: Config,
                 uiSprites: UiSpriteGroup, visibleSprites: CameraSpriteGroup):
        self.uiSprites = uiSprites

        self.clock = clock
        self.currentTimeInMS = currentTimeInMs
        self.dayLengthInMs = dayLengthInMs

        self.nightMask = Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), SRCALPHA)
        self.nightMask.fill((255, 255, 255))

        self.dawnStart = 6 / 24 * dayLengthInMs
        self.dayStart = 8 / 24 * dayLengthInMs
        self.eveningStart = 20 / 24 * dayLengthInMs
        self.nightStart = 22 / 24 * dayLengthInMs

        self.dawnLength = self.dayStart - self.dawnStart
        self.eveningLength = self.nightStart - self.eveningStart

        visibleSprites.sunlight = self.nightMask

        timesOfTheDay = [
            (self.dawnStart, Color(46, 54, 87)),
            (self.dawnLength, Color(205, 131, 122)),
            (self.eveningStart - self.dayStart, Color(254, 212, 86)),
            (self.eveningLength, Color(165, 91, 82)),
            (dayLengthInMs - self.nightStart, Color(46, 54, 87))
        ]
        self.dayCycleClock = DayNightClock(timesOfTheDay, self.currentTimeInMS, self.uiSprites, 200)

    def updateDayCycle(self):
        deltaTime = self.clock.get_time()
        self.currentTimeInMS = self.currentTimeInMS + deltaTime
        if self.currentTimeInMS >= self.dayLengthInMs:
            self.currentTimeInMS = 0

        brightness = self.calculateBrightness()
        self.nightMask.fill((brightness, brightness, brightness))
        self.dayCycleClock.update(self.currentTimeInMS)


    def calculateBrightness(self) -> int:
        if self.currentTimeInMS < self.dawnStart:
            brightness = 0
        elif self.currentTimeInMS < self.dayStart:
            brightness = (self.currentTimeInMS - self.dawnStart) / self.dawnLength * 255
        elif self.currentTimeInMS < self.eveningStart:
            brightness = 255
        elif self.currentTimeInMS < self.nightStart:
            brightness = 255 - (self.currentTimeInMS - self.eveningStart) / self.eveningLength * 255
        else:
            brightness = 0
        return brightness
