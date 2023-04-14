import pygame
from Config import Config
from pygame.time import Clock
from pygame import Surface, Color, SRCALPHA

from game.DayNightClock import DayNightClock
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup


class DayCycle:
    def __init__(self, currentTimeInMs: int, dayLengthInMs: int, clock: Clock, screen: Surface, config: Config,
                 uiSprites: UiSpriteGroup):
        self.uiSprites = uiSprites

        self.screen = screen
        self.clock = clock
        self.currentTime = currentTimeInMs
        self.dayLength = dayLengthInMs

        self.nightMask = Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), SRCALPHA)
        self.nightMask.fill((255, 255, 255))

        self.dawnStart = 6/24 * dayLengthInMs
        self.dayStart = 8/24 * dayLengthInMs
        self.eveningStart = 20/24 * dayLengthInMs
        self.nightStart = 22/24 * dayLengthInMs

        self.dawnLength = self.dayStart - self.dawnStart
        self.eveningLength = self.nightStart - self.eveningStart

        timesOfTheDay = [
            (self.dawnLength, Color(205, 131, 122)),
            (self.eveningStart - self.dayStart, Color(254, 212, 86)),
            (self.eveningStart, Color(165, 91, 82)),
            (self.nightStart - self.dawnStart, Color(46, 54, 87))
        ]
        self.dayCycleClock = DayNightClock(timesOfTheDay, self.currentTime, self.uiSprites, 200)

    def updateDayCycle(self):
        deltaTime = self.clock.get_time()
        self.currentTime += deltaTime
        if self.currentTime >= self.dayLength:
            print("a")
            self.currentTime = 0

        brightness = self.calculateBrightness()
        self.nightMask.fill((brightness, brightness, brightness))

        self.screen.blit(self.nightMask, (0, 0))
        self.dayCycleClock.update(self.currentTime)


    def calculateBrightness(self) -> int:
        if self.currentTime < self.dawnStart:
            brightness = 0
        elif self.currentTime < self.dayStart:
            brightness = (self.currentTime - self.dawnStart) / self.dawnLength * 255
        elif self.currentTime < self.eveningStart:
            brightness = 255
        elif self.currentTime < self.nightStart:
            brightness = 255 - (self.currentTime - self.eveningStart) / self.eveningLength * 255
        else:
            brightness = 0
        return brightness
