import random
from abc import ABC
from math import sqrt

from pygame import Vector2
from pygame.time import Clock

from game.entities.domain.Entity import Entity
from game.objects.domain.Object import Object
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class Mob(Entity, ABC):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 clock: Clock, entityData, sightRange: int, moveEveryMs: int,
                 minMoveMs: int, maxMoveMs: int):
        super().__init__(visibleSprites, obstacleSprites, entityData, clock)
        self.sightRange = sightRange
        self.isMoving = False
        self.movingTime = 0
        self.moveTime = 0
        self.timeBetweenMoves = 0
        self.moveEveryMs = moveEveryMs
        self.minMoveTimeMs = minMoveMs
        self.maxMoveTimeMs = maxMoveMs
        self.visibleSprites = visibleSprites

    def isInRange(self, target: Entity | Object, rangeDistance: int) -> bool:
        distance = sqrt((self.rect.centerx - target.rect.centerx) ** 2 +
                        (self.rect.centery - target.rect.centery) ** 2)
        return distance <= rangeDistance

    def isInSightRange(self, target: Entity | Object) -> bool:
        return self.isInRange(target, self.sightRange)

    def moveRandomly(self):
        dt = self.clock.get_time()
        if self.movingTime < self.moveTime:
            self.movingTime += dt
            self.move()
            return
        self.timeBetweenMoves += dt
        if self.timeBetweenMoves >= self.moveEveryMs:
            self.__buildRandomMove(self.minMoveTimeMs, self.maxMoveTimeMs)

    def __buildRandomMove(self, minMoveTime: int, maxMoveTime: int):
        self.timeBetweenMoves = 0
        self.movingTime = 0
        self.moveTime = random.randint(minMoveTime, maxMoveTime)
        self.direction = Vector2(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))

    def findClosestOtherEntity(self) -> Entity | None:
        closestEntity = None
        closestDistance = float('inf')
        for entity in self.visibleSprites.entities:
            if type(self) == type(entity):
                continue
            distance = sqrt((self.rect.centerx - entity.rect.x) ** 2 +
                            (self.rect.centery - entity.rect.y) ** 2)
            if distance < closestDistance:
                closestEntity = entity
                closestDistance = distance
        return closestEntity
