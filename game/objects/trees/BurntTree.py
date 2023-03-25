import pygame
from pygame import Rect
from pygame.math import Vector2
from pygame.sprite import Group

from config import ROOT_PATH
from game.items.Item import Item
from game.items.ToolType import ToolType
from game.objects.domain.CollisionObject import CollisionObject


class BurntTree(CollisionObject):
    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, midBottom: Vector2):
        image = pygame.image.load(f"{ROOT_PATH}/graphics/objects/trees/burntTree.png").convert_alpha()
        colliderRect = Rect((0, 0), (5, 5))
        colliderRect.midbottom = midBottom
        super().__init__(visibleGroup, obstaclesGroup,
                         midBottom, 1, ToolType.AXE, image, colliderRect)

    def interact(self) -> None:
        print("interacted with burnt trees")  # in the future there will be a real implementation

    def drop(self) -> None:
        Item(self.visibleGroup, self.rect.center)  # in the future there will be a real implementation
