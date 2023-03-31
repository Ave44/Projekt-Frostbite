from pygame import Surface, SRCALPHA
from pygame.time import Clock

from config import WINDOW_WIDTH, WINDOW_HEIGHT
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class DayCycle:
    def __init__(self, visibleSprites: CameraSpriteGroup, currentTimeInMs: int, dayLengthInMs: int, clock: Clock):
        self.clock = clock
        self.currentTime = currentTimeInMs
        self.dayLengthInMs = dayLengthInMs

        self.image = Surface((WINDOW_WIDTH, WINDOW_HEIGHT), SRCALPHA)
        self.image.fill((0, 0, 0))

        self.dawnStart = 6/24 * dayLengthInMs
        self.dayStart = 8/24 * dayLengthInMs
        self.eveningStart = 20/24 * dayLengthInMs
        self.nightStart = 22/24 * dayLengthInMs

        visibleSprites.sunlight = self.image

    def updateDayCycle(self):
        deltaTime = self.clock.get_time()
        self.currentTime = self.currentTime + deltaTime
        if self.currentTime >= self.dayLengthInMs:
            self.currentTime = 0

        alphaValue = self.calculateAlpha()
        self.image.fill((0, 0, 0))
        self.image.set_alpha(alphaValue)

    def calculateAlpha(self) -> int:
        if self.currentTime < self.dawnStart:
            alphaValue = 128
        elif self.currentTime < self.dayStart:
            alphaValue = (self.dayStart-self.currentTime) / (6/24 * self.dayLengthInMs) * 255
        elif self.currentTime < self.eveningStart:
            alphaValue = 0
        elif self.currentTime < self.nightStart:
            alphaValue = (self.currentTime-self.eveningStart) / (6/24 * self.dayLengthInMs) * 255
        else:
            alphaValue = 128
        return alphaValue
