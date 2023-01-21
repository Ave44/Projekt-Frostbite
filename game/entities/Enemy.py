import pygame
from pygame.math import Vector2
import operator

from game.entities.Entity import Entity


class Enemy(Entity):
    def __init__(self,
                 groups: pygame.sprite.Group,
                 obstacleSprites: pygame.sprite.Group,
                 enemyData,
                 sightRange: int):
        super(Enemy, self).__init__(groups, obstacleSprites, enemyData)
        self.sightRange = sightRange

    def isInSightRange(self, pos: tuple[int, int]) -> bool:
        sightRangeTuple = (self.sightRange, self.sightRange)
        minRange = tuple(map(operator.sub, self.rect.center, sightRangeTuple))
        maxRange = tuple(map(operator.add, self.rect.center, sightRangeTuple))
        
        if minRange < pos < maxRange:
            return True
        return False

    def followIfInRange(self, pos: Vector2) -> None:
        if self.isInSightRange((pos.x, pos.y)):
            self.destinationPosition = pos
        else:
            self.destinationPosition = None

    def update(self):
        self.move()
