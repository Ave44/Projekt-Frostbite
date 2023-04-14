from math import cos, radians, sin, pi

import pygame.image
from pygame import Surface, Vector2, SRCALPHA, Color, Rect
from pygame.sprite import Sprite
from pygame.transform import rotate

from Config import Config
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup


class DayNightClock(Sprite):
    def __init__(self, timesOfTheDay: list[tuple[float, Color]], currentTime: int, uiSprites: UiSpriteGroup, size: int):
        super().__init__(uiSprites)
        self.background = Surface(Vector2(size, size), SRCALPHA)
        self.backgroundRect = self.background.get_rect()

        self.image = Surface(Vector2(size, size), SRCALPHA)
        self.rect = self.image.get_rect()

        self.fullCycleTime = sum(list(map(lambda x: x[0], timesOfTheDay)))
        self.currentTime = currentTime
        self.radius = size / 2
        self.center = Vector2(self.radius, self.radius)

        self.updateBackground(timesOfTheDay)
        self.__drawClock()

    def updateBackground(self, newTimesOfTheDay: list[tuple[float, Color]]):
        startAngle = 0
        for newTimeOfTheDay in newTimesOfTheDay:
            arc = newTimeOfTheDay[0] / self.fullCycleTime * 360
            self.__drawBackground(newTimeOfTheDay[1], startAngle, startAngle + arc)
            startAngle += arc

        pygame.draw.circle(self.background, Color(0, 0 ,0), self.center, self.radius, 5)

    def __drawBackground(self, color: Color, startAngle: int, stopAngle: int):
        theta = startAngle
        while theta <= stopAngle:
            pygame.draw.line(self.background, color, self.center,
                             (self.center.x + (self.radius-5) * cos(radians(theta - 90)),
                              self.center.y + (self.radius-5) * sin(radians(theta - 90))),
                             2)
            theta += 0.01

    def __drawClockHand(self):
        hourAngle = ((self.currentTime % self.fullCycleTime) / self.fullCycleTime) * 2 * pi
        hourAngle -= pi / 2

        handX = self.center.x + self.radius * cos(hourAngle)
        handY = self.center.y + self.radius * sin(hourAngle)
        handEnd = (handX, handY)

        pygame.draw.line(self.image, Color(0, 0, 0), self.center, handEnd, 3)

    def __drawClock(self):
        self.image.blit(self.background, self.backgroundRect)
        self.__drawClockHand()

    def update(self, newCurrentTime: int):
        self.currentTime = newCurrentTime
        self.__drawClock()
