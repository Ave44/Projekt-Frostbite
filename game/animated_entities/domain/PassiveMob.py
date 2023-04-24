from abc import ABC
from random import random

from pygame import Vector2

from game.animated_entities.domain.AnimatedEntity import AnimatedEntity
from game.entities.domain.Entity import Entity
from game.animated_entities.domain.Mob import Mob


class PassiveMob(Mob, ABC):
    def runAway(self, fromEntity: Entity | AnimatedEntity):
        xOffset = self.rect.centerx - fromEntity.rect.centerx
        yOffset = self.rect.bottom - fromEntity.rect.bottom
        if xOffset == 0 and yOffset == 0:
            xOffset = random()
            yOffset = random()
        self.direction = Vector2(xOffset, yOffset)
        self.move()

    def localUpdate(self):
        closestOtherEntity = self.findClosestOtherEntity()
        if closestOtherEntity and self.isInSightRange(closestOtherEntity):
            self.runAway(closestOtherEntity)
        else:
            self.moveRandomly()
