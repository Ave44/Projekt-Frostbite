import pygame
from pygame import Surface
from pygame.time import Clock

from config import WINDOW_WIDTH, WINDOW_HEIGHT


class DayCycle:
    def __init__(self, currentTimeInMs: int, dayLengthInMs: int, clock: Clock, screen: Surface):
        self.screen = screen
        self.clock = clock
        self.currentTimeInMs = currentTimeInMs
        self.dayLengthInMs = dayLengthInMs
        self.blackSurface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.blackSurface.fill((0, 0, 0))

        self.beginningOfNightTime = 21 / 24 * dayLengthInMs
        self.nightTime = dayLengthInMs
        self.beginningOfDayTime = 6 / 24 * dayLengthInMs
        self.dayTime = 9 / 24 * dayLengthInMs
        self.light = pygame.image.load("./graphics/lights/light.png")

        self.filter = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

    def updateDayCycle(self):
        deltaTime = self.clock.get_time()
        self.currentTimeInMs = self.currentTimeInMs + deltaTime
        if self.currentTimeInMs >= self.dayLengthInMs:
            self.currentTimeInMs = 0

        if self.beginningOfNightTime < self.currentTimeInMs <= self.nightTime:
            alphaValue = (self.currentTimeInMs - self.beginningOfNightTime) / (6 / 24 * self.dayLengthInMs) * 255
        elif self.beginningOfDayTime < self.currentTimeInMs <= self.dayTime:
            alphaValue = (self.dayTime - self.currentTimeInMs) / (6 / 24 * self.dayLengthInMs) * 255
        elif self.dayTime < self.currentTimeInMs <= self.beginningOfNightTime:
            alphaValue = 0
        else:
            alphaValue = 128

        self.filter.fill(pygame.color.Color(255, 255, 255))
        self.filter.blit(self.light, (pygame.mouse.get_pos()[0] - 50, pygame.mouse.get_pos()[1] - 50))

        pygame.display.get_surface().blit(self.filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.blackSurface.set_alpha(alphaValue)
        pygame.display.get_surface().blit(self.blackSurface, (0, 0))
