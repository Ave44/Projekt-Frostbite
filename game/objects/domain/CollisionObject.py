from abc import ABC

from pygame import Rect
from pygame.math import Vector2
from pygame.sprite import Group
from pygame.surface import Surface

from typing import Type
from game.objects.domain.Object import Object


class CollisionObject(Object, ABC):
    def __init__(self, visibleSprites: Group, obstacleSprites: Group,
                 midbottom: Vector2, maxDurability: int, toolType: Type,
                 image: Surface, colliderRect: Rect, currentDurability: int = None):
        Object.__init__(self, visibleSprites, midbottom, maxDurability, toolType, image, currentDurability)
        obstacleSprites.add(self)
        self.obstacleSprites = obstacleSprites
        self.colliderRect = colliderRect
