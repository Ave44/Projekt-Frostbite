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
                 color: str,
                 targetColor: str):
        super(Bar, self).__init__()

        self.maxValue = maxValue
        self.currentValue = currentValue
        self.displayValue = currentValue

        self.barHeight = barHeight
        self.barLength = barLength
        self.color = color
        self.targetColor = targetColor

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

    def getDisplayValueSurfaceAndRect(self) -> tuple[Surface, Rect]:
        return self.getSurfaceAndRect(self.getValueLength(self.displayValue), self.barHeight, self.targetColor)

    def getCurrentValueSurfaceAndRect(self) -> tuple[Surface, Rect]:
        return self.getSurfaceAndRect(self.getValueLength(self.currentValue), self.barHeight, self.color)

    def getSurfaceAndRect(self, length: int, height: int, color: str) -> tuple[Surface, Rect]:
        surface = pygame.Surface([length, height])
        surface.fill(color)

        rect = surface.get_rect()
        rect.topleft = self.pos
        return surface, rect

    def getValueRatio(self, value) -> int:
        return value / self.maxValue

    def getValueLength(self, value) -> int:
        return self.barLength * self.getValueRatio(value)

    def draw(self, screen: Surface):
        (borderSurface, borderRect) = self.getBorderSurfaceAndRect()
        screen.blit(borderSurface, borderRect)

        (bgSurface, bgRect) = self.getBackgroundSurfaceAndRect()
        screen.blit(bgSurface, bgRect)

        if self.displayValue < self.currentValue:
            self.displayValue += 1

            (currentSurface, currentRect) = self.getCurrentValueSurfaceAndRect()
            currentSurface.fill(self.targetColor)
            screen.blit(currentSurface, currentRect)

            (displayValSurface, displayValRect) = self.getDisplayValueSurfaceAndRect()
            displayValSurface.fill(self.color)
            screen.blit(displayValSurface, displayValRect)

        if self.displayValue > self.currentValue:
            self.displayValue -= 1

            (displayValSurface, displayValRect) = self.getDisplayValueSurfaceAndRect()
            screen.blit(displayValSurface, displayValRect)

            (currentSurface, currentRect) = self.getCurrentValueSurfaceAndRect()
            screen.blit(currentSurface, currentRect)

        if self.displayValue == self.currentValue:
            (currentSurface, currentRect) = self.getCurrentValueSurfaceAndRect()
            screen.blit(currentSurface, currentRect)


    def update(self, newCurrentValue: int):
        self.currentValue = newCurrentValue


