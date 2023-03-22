import pygame
from pygame import Vector2
from pygame.time import Clock

from config import ROOT_PATH
from game.entities.Rabbit import Rabbit
from game.items.ToolType import ToolType
from game.objects.domain.Object import Object
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class RabbitHole(Object):
    def __init__(self, visibleGroup: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 midBottom: Vector2, clock: Clock):
        image = pygame.image.load(f"{ROOT_PATH}/graphics/objects/rabbit_hole.png")
        super().__init__(visibleGroup, midBottom, 50, ToolType.SHOVEL, image)
        self.rabbits = []
        self.daysFromRabbitsChange = 0
        self.obstacleSprites = obstacleSprites
        self.clock = clock

        self.spawnRabbit()
        self.spawnRabbit()
        self.spawnRabbit()

    def spawnRabbit(self):
        newRabbit = Rabbit(self.visibleGroup, self.obstacleSprites, self.clock,
                           Vector2(self.rect.centerx, self.rect.centery))
        self.rabbits.append(newRabbit)
        self.daysFromRabbitsChange = 0

    def deleteDeadRabbit(self):
        newRabbits = list(filter(lambda rabbit: rabbit.currentHealth > 0, self.rabbits))
        if len(self.rabbits) != len(newRabbits):
            self.daysFromRabbitsChange = 0
            self.rabbits = newRabbits

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
        self.deleteDeadRabbit()
        self.releaseRabbits(True)

    def interact(self) -> None:
        print("interacted with rabbit hole")

    def onNewDay(self):
        self.deleteDeadRabbit()
        self.releaseRabbits()

        if len(self.rabbits) >= 3:
            return

        if self.daysFromRabbitsChange < 10:
            self.daysFromRabbitsChange += 1
            return

        self.spawnRabbit()

    def onEvening(self):
        self.deleteDeadRabbit()
        self.hideRabbits()
