from abc import ABC
from pygame import Vector2, Surface
from pygame.time import Clock
from game.entities.domain.Entity import Entity
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites
class AnimatedEntity(Entity,ABC):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: dict, loadedSounds: dict, clock: Clock, entityData, sightRange: int, moveEveryMs: int,
                 minMoveMs: int, maxMoveMs: int, midbottom: Vector2, currHealth: int = None):
        Entity.__init__(self, visibleSprites, obstacleSprites, entityData, loadedImages, loadedSounds, clock, midbottom, currHealth)
        self.sightRange = sightRange
        self.isMoving = False
        self.movingTime = 0
        self.moveTime = 0
        self.timeBetweenMoves = 0
        self.moveEveryMs = moveEveryMs
        self.minMoveTimeMs = minMoveMs
        self.maxMoveTimeMs = maxMoveMs
        self.visibleSprites = visibleSprites

    def __changeImages(self, newImageUp: Surface, newImageDown: Surface, newImageLeft: Surface, newImageRight: Surface):
        if self.image == self.imageUp:
            self.image = newImageUp
        elif self.image == self.imageDown:
            self.image = newImageDown
        elif self.image == self.imageLeft:
            self.image = newImageLeft
        else:
            self.image = newImageRight

        self.imageUp = newImageUp
        self.imageDown = newImageDown
        self.imageLeft = newImageLeft
        self.imageRight = newImageRight
