from pygame import Surface, SRCALPHA
from pygame.time import Clock

from config import WINDOW_WIDTH, WINDOW_HEIGHT
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class DayCycle:
    def __init__(self, visibleSprites: CameraSpriteGroup, currentTimeInMs: int, dayLengthInMs: int, clock: Clock):
        self.clock = clock
        self.currentTime = currentTimeInMs
        self.dayLengthInMs = dayLengthInMs

        self.nightMask = Surface((WINDOW_WIDTH, WINDOW_HEIGHT), SRCALPHA)
        self.nightMask.fill((255, 255, 255))

        self.dawnStart = 6/24 * dayLengthInMs
        self.dayStart = 8/24 * dayLengthInMs
        self.eveningStart = 20/24 * dayLengthInMs
        self.nightStart = 22/24 * dayLengthInMs

        self.dawnLength = self.dayStart - self.dawnStart
        self.eveningLength = self.nightStart - self.eveningStart

        visibleSprites.sunlight = self.nightMask

    def updateDayCycle(self):
        deltaTime = self.clock.get_time()
        self.currentTime = self.currentTime + deltaTime
        if self.currentTime >= self.dayLengthInMs:
            self.currentTime = 0

        brightness = self.calculateBrightness()
        self.nightMask.fill((brightness, brightness, brightness))

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
