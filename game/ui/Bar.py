from pygame import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface

from constants import BG_COLOR, BORDER_COLOR, BORDER_SIZE


class Bar(Sprite):
    def __init__(self,
                 center: Vector2,
                 maxValue: int,
                 currentValue: int,
                 barHeight: int,
                 barLength: int,
                 mainColor: tuple[int, int, int],
                 increaseColor: tuple[int, int, int],
                 decreaseColor: tuple[int, int, int]):
        super().__init__()

        self.maxValue = maxValue
        self.currentValue = currentValue
        self.displayValue = currentValue
        self.valueRatio = barLength / maxValue

        self.barHeight = barHeight
        self.barLength = barLength

        self.mainColor = mainColor
        self.increaseColor = increaseColor
        self.decreaseColor = decreaseColor

        self.center = center
        self.bgSurface = Surface([barLength, barHeight])
        self.bgSurface.fill(BG_COLOR)
        self.bgRect = Rect(center.x - barLength/2, center.y - barHeight/2, barLength, barHeight)

        self.borderSurface = Surface([barLength + BORDER_SIZE * 2, barHeight + BORDER_SIZE * 2])
        self.borderSurface.fill(BORDER_COLOR)
        self.borderRect = Rect(center.x - barLength / 2 - BORDER_SIZE,
                               center.y - barHeight / 2 - BORDER_SIZE,
                               barLength + BORDER_SIZE * 2,
                               barHeight + BORDER_SIZE * 2)

    def drawBarSurface(self, screen: Surface, value: int, color: tuple[int, int, int]):
        length = value * self.valueRatio
        surface = Surface([length, self.barHeight])
        surface.fill(color)

        rect = surface.get_rect()
        rect.topleft = self.bgRect.topleft

        screen.blit(surface, rect)

    def draw(self, screen: Surface):
        screen.blit(self.borderSurface, self.borderRect)
        screen.blit(self.bgSurface, self.bgRect)

        if self.displayValue == self.currentValue:
            self.drawBarSurface(screen, self.currentValue, self.mainColor)
        elif self.displayValue < self.currentValue:
            self.displayValue += 1
            self.drawBarSurface(screen, self.currentValue, self.increaseColor)
            self.drawBarSurface(screen, self.displayValue, self.mainColor)
        else:
            self.displayValue -= 1
            self.drawBarSurface(screen, self.displayValue, self.decreaseColor)
            self.drawBarSurface(screen, self.currentValue, self.mainColor)

    def update(self, newCurrentValue: int):
        self.currentValue = newCurrentValue
