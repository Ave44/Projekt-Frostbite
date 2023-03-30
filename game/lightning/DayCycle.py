import pygame
from pygame.time import Clock

from config import WINDOW_WIDTH, WINDOW_HEIGHT
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class DayCycle:
    def __init__(self, visibleSprites: CameraSpriteGroup, currentTimeInMs: int, dayLengthInMs: int, clock: Clock):
        super().__init__()
        visibleSprites.sunlight = self

        self.clock = clock
        self.currentTimeInMs = currentTimeInMs
        self.dayLengthInMs = dayLengthInMs

        self.image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.image.fill((0, 0, 0))

        self.beginningOfNightTime = 21/24 * dayLengthInMs
        self.nightTime = dayLengthInMs
        self.beginningOfDayTime = 6/24 * dayLengthInMs
        self.dayTime = 9/24 * dayLengthInMs

    def updateDayCycle(self):
        deltaTime = self.clock.get_time()
        self.currentTimeInMs = self.currentTimeInMs + deltaTime
        if self.currentTimeInMs >= self.dayLengthInMs:
            self.currentTimeInMs = 0

        alphaValue = self.calculateAlpha()
        self.image.fill((0, 0, 0))
        self.image.set_alpha(alphaValue)

    def calculateAlpha(self) -> int:
        if self.beginningOfNightTime < self.currentTimeInMs <= self.nightTime:
            alphaValue = (self.currentTimeInMs-self.beginningOfNightTime) / (6/24 * self.dayLengthInMs) * 255
        elif self.beginningOfDayTime < self.currentTimeInMs <= self.dayTime:
            alphaValue = (self.dayTime-self.currentTimeInMs) / (6/24 * self.dayLengthInMs) * 255
        elif self.dayTime < self.currentTimeInMs <= self.beginningOfNightTime:
            alphaValue = 0
        else:
            alphaValue = 128
        return alphaValue
