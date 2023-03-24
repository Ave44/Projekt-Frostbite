from abc import ABC

from pygame import Rect
from pygame.math import Vector2
from pygame.sprite import Group, Sprite
from pygame.surface import Surface

from game.items.domain.ToolType import ToolType
from game.objects.domain.Object import Object


class CollisionObject(Object, ABC):
    def __init__(self, visibleGroup: Group, obstaclesGroup: Group,
                 midBottom: Vector2, durability: int, toolType: ToolType,
                 image: Surface, colliderRect: Rect):
        super().__init__(visibleGroup, midBottom, durability, toolType, image)
        Sprite.__init__(self, obstaclesGroup, visibleGroup)
        self.obstaclesGroup = obstaclesGroup
        self.colliderRect = colliderRect
