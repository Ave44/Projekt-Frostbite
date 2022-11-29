import pygame
from pygame import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface

from config import *


class Bar(Sprite):
    def __init__(self,
                 topLeftPosition: Vector2,
                 maxValue: int, currentValue: int,
                 barHeight: int,
                 barLength: int,
                 color: str):
        super(Bar, self).__init__()

        self.maxValue = maxValue
        self.currentValue = currentValue

        self.barHeight = barHeight
        self.barLength = barLength
        self.color = color

        self.pos = topLeftPosition

    def getBorderSurfaceAndRect(self) -> tuple[Surface, Rect]:
        (bgSurface, bgRect) = self.getBackgroundSurfaceAndRect()
        bgSize = bgSurface.get_size()

        borderSurface = Surface([bgSize[0] + UI_BORDER_SIZE * 2, bgSize[1] + UI_BORDER_SIZE * 2])
        borderSurface.fill(UI_BORDER_COLOR)

        borderRect = bgRect.copy()
        borderRect = borderRect.move(-UI_BORDER_SIZE, -UI_BORDER_SIZE)

        return borderSurface, borderRect

    def getBackgroundSurfaceAndRect(self) -> tuple[Surface, Rect]:
        return self.getSurfaceAndRect(self.barLength, self.barHeight, UI_BG_COLOR)

    def getValueSurfaceAndRect(self) -> tuple[Surface, Rect]:
        return self.getSurfaceAndRect(int(self.getCurrentLength()), self.barHeight, self.color)

    def getSurfaceAndRect(self, length: int, height: int, color: str) -> tuple[Surface, Rect]:
        surface = pygame.Surface([length, height])
        surface.fill(color)

        rect = surface.get_rect()
        rect.topleft = self.pos
        return surface, rect

    def getValueRatio(self) -> float:
        return self.currentValue / self.maxValue

    def getCurrentLength(self) -> float:
        return self.barLength * self.getValueRatio()

    def draw(self, screen: Surface):
        (borderSurface, borderRect) = self.getBorderSurfaceAndRect()
        screen.blit(borderSurface, borderRect)

        (bgSurface, bgRect) = self.getBackgroundSurfaceAndRect()
        screen.blit(bgSurface, bgRect)

        (valSurface, valRect) = self.getValueSurfaceAndRect()
        screen.blit(valSurface, valRect)

    def update(self, newCurrentValue: int):
        self.currentValue = newCurrentValue


