import pygame
from pygame import Vector2
from pygame.time import Clock

from config import ROOT_PATH
from game.entities.Rabbit import Rabbit
from game.items.domain.ToolType import ToolType
from game.objects.domain.Object import Object
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class RabbitHole(Object):
    def __init__(self, visibleGroup: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 midBottom: Vector2, clock: Clock):
        image = pygame.image.load(f"{ROOT_PATH}/graphics/objects/rabbit_hole.png").convert_alpha()
        super().__init__(visibleGroup, midBottom, 50, ToolType.SHOVEL, image)
        self.rabbits = []
        self.daysFromRabbitsChange = 0
        self.obstacleSprites = obstacleSprites
        self.clock = clock

        self.spawnRabbit()
        self.spawnRabbit()
        self.spawnRabbit()

    def spawnRabbit(self):
        pos = Vector2(self.rect.centerx, self.rect.centery)
        newRabbit = Rabbit(self.visibleGroup, self.obstacleSprites, self.clock, pos, self)
        self.rabbits.append(newRabbit)
        self.daysFromRabbitsChange = 0

    def releaseRabbits(self, forever: bool = False):
        for rabbit in self.rabbits:
            if not rabbit.isInHome:
                continue
            if forever:
                rabbit.isHomeless = True
            rabbit.goOut()

    def hideRabbits(self):
        for rabbit in self.rabbits:
            if not rabbit.isInHome:
                rabbit.runHome()

    def drop(self) -> None:
        self.releaseRabbits(True)

    def interact(self) -> None:
        print("interacted with rabbit hole")

    def onNewDay(self):
        self.releaseRabbits()

        if len(self.rabbits) >= 3:
            return

        if self.daysFromRabbitsChange < 10:
            self.daysFromRabbitsChange += 1
            return

        self.spawnRabbit()

    def onEvening(self):
        self.hideRabbits()
