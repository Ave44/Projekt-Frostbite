import random
from abc import ABC

from pygame import Vector2
from pygame.time import Clock

from game.animated_entities.domain.AnimatedEntity import AnimatedEntity
from game.entities.domain.Entity import Entity
from game.objects.domain.Object import Object
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class Mob(AnimatedEntity, ABC):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: dict, loadedSounds: dict, clock: Clock, entityData, midbottom: Vector2, currHealth: int = None):
        AnimatedEntity.__init__(self, visibleSprites, obstacleSprites, entityData, loadedImages, loadedSounds, clock, midbottom, currHealth)
        self.sightRange = entityData["sightRange"]
        self.isMoving = False
        self.movingTime = 0
        self.moveTime = 0
        self.timeBetweenMoves = 0
        self.moveEveryMs = entityData["moveEveryMs"]
        self.minMoveTimeMs = entityData["minMoveTimeMs"]
        self.maxMoveTimeMs = entityData["maxMoveTimeMs"]
        self.visibleSprites = visibleSprites

    def isInSightRange(self, target: Entity | Object | AnimatedEntity) -> bool:
        return self.isInRange(Vector2(target.rect.midbottom), self.sightRange)

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
