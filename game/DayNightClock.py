from math import cos, radians, sin

import pygame.image
from pygame import Surface, Vector2, SRCALPHA
from pygame.sprite import Sprite
from pygame.transform import rotate

from Config import Config
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup


class DayNightClock(Sprite):
    def __init__(self, backgroundImage: Surface, fullCycleTimeMS: int, currentTimeMS: int, uiSprites: UiSpriteGroup,
                 clockHand: Surface):
        super().__init__(uiSprites)
        self.image = Surface(Vector2(200, 200), SRCALPHA)
        self.rect = self.image.get_rect()
        self.fullCycleTimeMS = fullCycleTimeMS
        self.currentTimeMS = currentTimeMS

        # imageRect = self.image.get_rect()
        # r = Vector2(imageRect.midtop[0], imageRect.midtop[1])
        # x = Vector2(clockHand.get_width() // 2, 0)
        # angle = 30
        # clockHand = rotate(clockHand, -angle)

        # c = Vector2(90 - angle + 15, 0)
        # if angle < 90:
        #     d = clockHand.get_rect(bottomleft = Vector2(backgroundImage.get_width() // 2, backgroundImage.get_height() // 2) - c)
        # elif angle == 90:
        #     d = clockHand.get_rect(midleft = Vector2(backgroundImage.get_width() // 2, backgroundImage.get_height() // 2) - c)
        # elif angle <= 180:
        #     d = clockHand.get_rect(topright = Vector2(backgroundImage.get_width() // 2, backgroundImage.get_height() // 2) + c)
        # else:
        #     d = (0, 0)

        # pygame.draw.line()
        # self.image.blit(clockHand, d)

        def pie(scr, color, center, radius, start_angle, stop_angle):
            theta = start_angle
            while theta <= stop_angle:
                pygame.draw.line(scr, color, center,
                                 (center[0] + radius * cos(radians(theta - 90)) , center[1] + radius * sin(radians(theta - 90))),
                                 2)
                theta += 0.01

        pie(self.image, (205, 131, 122), Vector2(100, 100), 100, 0, 30)
        pie(self.image, (254, 212, 86), Vector2(100, 100), 100, 31, 210)
        pie(self.image, (165, 91, 82), Vector2(100, 100), 100, 211, 240)
        pie(self.image, (46, 54, 87), Vector2(100, 100), 100, 241, 359)

