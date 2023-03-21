from abc import ABC

from pygame import Vector2

from game.entities.domain.Entity import Entity
from game.entities.domain.Mob import Mob


class PassiveMob(Mob, ABC):
    def runAway(self, fromEntity: Entity):
        xOffset = -fromEntity.rect.x + self.rect.centerx
        yOffset = -fromEntity.rect.y + self.rect.bottom
        self.direction = Vector2(xOffset, yOffset)
        self.move()

    def localUpdate(self):
        closestOtherEntity = self.findClosestOtherEntity()
        if closestOtherEntity and self.isInSightRange(closestOtherEntity):
            self.runAway(closestOtherEntity)
        else:
            self.moveRandomly()
