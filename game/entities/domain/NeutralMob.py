from abc import ABC

from game.entities.domain.AggressiveMob import EnemyMob
from game.entities.domain.State import State


class NeutralMob(EnemyMob, ABC):
    def localUpdate(self):
        if not self.target and self.state == State.DAMAGED:
            closestEntity = self.findClosestOtherEntity()
            if closestEntity and self.isInSightRange(closestEntity):
                self.target = closestEntity
                self.moveToOrAttack(self.target)
                return
            self.moveRandomly()
            return

        if not self.isInSightRange(self.target):
            self.target = None
            self.destinationPosition = None
            return

        self.moveToOrAttack(self.target)
