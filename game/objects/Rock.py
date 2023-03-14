import pygame
from pygame.math import Vector2
from pygame.sprite import Group

from config import ROOT_PATH
from game.items.Sword import Sword
from game.items.ToolType import ToolType
from game.objects.domain.Object import Object


class Rock(Object):
    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, center: Vector2()):
        image = pygame.image.load(f"{ROOT_PATH}/graphics/objects/rock.png")
        super().__init__(visibleGroup, obstaclesGroup,
                         center, 40, ToolType.PICKAXE, image)

    def interact(self) -> None:
        # do something
        pass

    def drop(self) -> None:
        Sword(self.visibleGroup, self.rect.center)
