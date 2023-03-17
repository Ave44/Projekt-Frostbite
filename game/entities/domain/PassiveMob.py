import math
from abc import ABC

from pygame import Vector2
from pygame.time import Clock

from game.entities.domain.Entity import Entity
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class PassiveMob(Entity, ABC):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 clock: Clock, entityData, sightRange: int):
        super().__init__(visibleSprites, obstacleSprites, entityData, clock)
        self.sightRange = sightRange

    def runAway(self, fromEntity: Entity):
        xOffset = -fromEntity.rect.x + self.rect.centerx
        yOffset = -fromEntity.rect.y + self.rect.bottom
        self.direction = Vector2(xOffset, yOffset)
        self.move()

    def runAwayIfEntityTooClose(self, entity: Entity):
        distance = math.sqrt((self.rect.centerx - entity.rect.x) ** 2 +
                             (self.rect.centery - entity.rect.y) ** 2)
        if distance <= self.sightRange:
            self.runAway(entity)
