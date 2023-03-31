import pygame
from pygame.math import Vector2
from pygame.sprite import Group

from config import ROOT_PATH
from game.items.Sword import Sword
from game.items.domain.ToolType import ToolType
from game.lightning.Glowing import Glowing
from game.lightning.LightSize import LightSize
from game.objects.domain.Object import Object


class Grass(Object, Glowing):
    def __init__(self, visibleGroup: Group, midBottom: Vector2):
        image = pygame.image.load(f"{ROOT_PATH}/graphics/objects/grass.png").convert_alpha()
        super().__init__(visibleGroup,
                         midBottom, 1, ToolType.SHOVEL, image)
        Glowing.__init__(self, LightSize.SMALL)

    def interact(self) -> None:
        # do something
        pass

    def drop(self) -> None:
        Sword(self.visibleGroup, self.rect.midBottom)
