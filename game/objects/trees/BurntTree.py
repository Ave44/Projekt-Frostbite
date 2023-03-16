import pygame
from pygame.math import Vector2
from pygame.sprite import Group

from config import ROOT_PATH
from game.items.ToolType import ToolType
from game.objects.domain.Object import Object


class BurntTree(Object):
    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, bottomCenter: Vector2):
        image = pygame.image.load(f"{ROOT_PATH}/graphics/objects/trees/burntTree.png")
        super().__init__(visibleGroup, obstaclesGroup,
                         bottomCenter, 1, ToolType.AXE, image)

    def interact(self) -> None:
        print("interacted with burnt trees")  # in the future there will be a real implementation

    def drop(self) -> None:
        Item(self.visibleGroup, self.rect.center)  # in the future there will be a real implementation
