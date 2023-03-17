import pygame
from pygame import Rect
from pygame.math import Vector2
from pygame.sprite import Group

from config import ROOT_PATH
from game.items.Sword import Sword
from game.items.ToolType import ToolType
from game.objects.domain.CollisionObject import CollisionObject


class Rock(CollisionObject):
    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, midBottom: Vector2):
        image = pygame.image.load(f"{ROOT_PATH}/graphics/objects/rock.png")
        coliderRect = Rect((0, 0), (10, 10))
        coliderRect.midbottom = midBottom

        super().__init__(visibleGroup, obstaclesGroup,
                         midBottom, 40, ToolType.PICKAXE, image, coliderRect)

    def interact(self) -> None:
        # do something
        pass

    def drop(self) -> None:
        Sword(self.visibleGroup, self.rect.center)
