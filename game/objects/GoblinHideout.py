import pygame
from pygame import Vector2
from pygame.time import Clock

from config import ROOT_PATH
from game.entities.Goblin import Goblin
from game.items.domain.ToolType import ToolType
from game.objects.domain.Object import Object
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class GoblinHideout(Object):
    def __init__(self, visibleGroup: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 midBottom: Vector2, clock: Clock):
        image = pygame.image.load(f"{ROOT_PATH}/graphics/objects/goblin_hideout.png").convert_alpha()
        super().__init__(visibleGroup, midBottom, 50, ToolType.SHOVEL, image)
        self.goblins = []
        self.daysFromGoblinsChange = 0
        self.obstacleSprites = obstacleSprites
        self.clock = clock

        self.spawnGoblin()
        self.spawnGoblin()

    def spawnGoblin(self):
        pos = Vector2(self.rect.centerx, self.rect.centery)
        newGoblin = Goblin(self.visibleGroup, self.obstacleSprites, self.clock, pos, self)
        self.goblins.append(newGoblin)
        self.daysFromGoblinsChange = 0

    def releaseGoblins(self, forever: bool = False):
        for goblin in self.goblins:
            if not goblin.isInHome:
                continue
            if forever:
                goblin.isHomeless = True
            goblin.goOut()

    def drop(self) -> None:
        self.releaseGoblins(True)

    def interact(self) -> None:
        print("interacted with goblin hideout")

    def releaseGoblins(self, forever: bool = False):
        for goblin in self.goblins:
            if not goblin.isInHome:
                continue
            if forever:
                goblin.isHomeless = True
            goblin.goOut()

    def onNewDay(self):
        self.releaseGoblins()

        if len(self.goblins) >= 2:
            return

        if self.daysFromGoblinsChange < 2:
            self.daysFromGoblinsChange += 1
            return

        self.spawnGoblin()

    def onEvening(self):
        self.hideGoblins()
