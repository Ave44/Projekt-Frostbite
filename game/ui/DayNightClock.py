from math import cos, radians, sin

import pygame.image
from pygame import Surface, Rect, Vector2, Color, SRCALPHA
from pygame.font import Font

from constants import CLOCK_OUTLINE, CLOCK_OUTLINE_SHADOW, SHADOW, BORDER_SIZE, FONT_COLOR, FONT, FONT_SIZE


class DayNightClock():
    def __init__(self, dayLengthMs: int, daySegments: int,
                 currentTime: int, currentDay: int, size: int):
        self.dayLengthMs = dayLengthMs
        self.currentDay = currentDay
        self.currentTime = currentTime
        self.radius = size / 2
        self.center = Vector2(self.radius, self.radius)
        self.font = Font(FONT, FONT_SIZE)

        self.background = Surface(Vector2(size, size), SRCALPHA)
        self.backgroundOutline = Surface(Vector2(size, size), SRCALPHA)
        self.createBackgroundOutline(daySegments)
        self.drawCircleCutout(self.background, 0, 360, 0.1, 0, self.radius / 2 - BORDER_SIZE, SHADOW)

        self.hand = Surface(Vector2(size, size), SRCALPHA)
        pygame.draw.line(self.hand, CLOCK_OUTLINE,
                         (self.center.x, self.center.y - self.radius),
                         (self.center.x, self.center.y - self.radius / 2), 4)

    def updateBackground(self, dayPhases: list[tuple[float, Color]]):
        for dayPhaseIndex in range(len(dayPhases)):
            angleStart = dayPhases[dayPhaseIndex]['start'] / self.dayLengthMs * 360
            angleEnd = dayPhases[(dayPhaseIndex + 1) % len(dayPhases)]['start'] / self.dayLengthMs * 360
            color = dayPhases[dayPhaseIndex]['color']
            if angleStart > angleEnd:
                self.drawCircleCutout(self.background, angleStart, 360, 0.02, self.radius / 2, self.radius, color)
                self.drawCircleCutout(self.background, 0, angleEnd, 0.02, self.radius / 2, self.radius, color)
            else:
                self.drawCircleCutout(self.background, angleStart, angleEnd, 0.02, self.radius / 2, self.radius, color)

        self.background.blit(self.backgroundOutline, (0, 0))

    def createBackgroundOutline(self, daySegments: int):
        segmentAngle = 360 / daySegments

        halfDaySegments = int(daySegments / 2)
        for segment in range(halfDaySegments):
            angleStart = (segment * 2) * segmentAngle
            angleEnd = angleStart + segmentAngle
            self.drawCircleCutout(self.backgroundOutline, angleStart, angleEnd, 0.02, self.radius / 2, self.radius, CLOCK_OUTLINE_SHADOW)

        self.drawCircleCutout(self.backgroundOutline, 0, 360, segmentAngle, self.radius / 2, self.radius, CLOCK_OUTLINE)

        self.drawCircleCutout(self.backgroundOutline, 0, 360, 0.02, self.radius - BORDER_SIZE + 1, self.radius, CLOCK_OUTLINE)
        self.drawCircleCutout(self.backgroundOutline, 0, 360, 0.1, self.radius / 2 - BORDER_SIZE + 1, self.radius / 2, CLOCK_OUTLINE)

    def drawCircleCutout(self, surface: Surface, angleStart: float, angleEnd: float, angleStep: float, radiusStart: float, radiusEnd: float, color: Color):
        angle = angleStart
        while angle <= angleEnd:
            pygame.draw.line(surface, color,
                             (self.center.x + radiusStart * cos(radians(angle - 90)),
                              self.center.y + radiusStart * sin(radians(angle - 90))),

                             (self.center.x + radiusEnd * cos(radians(angle - 90)),
                              self.center.y + radiusEnd * sin(radians(angle - 90))),
                             1)
            angle += angleStep

    def draw(self, displaySurface: Surface, rect: Rect):
        displaySurface.blit(self.background, rect)
        dayCount = self.font.render(str(self.currentDay), True, FONT_COLOR)
        dayCountRect = dayCount.get_rect(center=rect.center)
        displaySurface.blit(dayCount, dayCountRect)

        angle = (self.currentTime / self.dayLengthMs) * -360
        rotatedHand = pygame.transform.rotate(self.hand, angle)
        handPosition = (rect.centerx - rotatedHand.get_width() / 2, rect.centery - rotatedHand.get_height() / 2)

        displaySurface.blit(rotatedHand, handPosition)

    def update(self, newCurrentTime: int):
        self.currentTime = newCurrentTime
