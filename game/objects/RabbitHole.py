import pygame
from pygame import Vector2
from pygame.sprite import Group

from config import ROOT_PATH
from game.items.ToolType import ToolType
from game.objects.domain.Object import Object


class RabbitHole(Object):
    def __init__(self, visibleGroup: Group, midBottom: Vector2):
        image = pygame.image.load(f"{ROOT_PATH}/graphics/objects/rabbit_hole.png")
        super().__init__(visibleGroup, midBottom, 50, ToolType.SHOVEL, image)
        self.connectedRabbit = []

    def hideRabbit(self, rabbit: Rabbit):
        pass

    def releaseRabbits(self):
        pass

    def spawnRabbit(self):
        pass

    def drop(self) -> None:
        pass

    def interact(self) -> None:
        pass
