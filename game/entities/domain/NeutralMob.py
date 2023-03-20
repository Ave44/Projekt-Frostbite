from abc import ABC

from game.entities.domain.AggressiveMob import AggressiveMob
from game.entities.domain.State import State


class NeutralMob(AggressiveMob, ABC):
    def localUpdate(self):
        if not self.target and self.state != State.DAMAGED:
            return

        if not self.target:
            closestEntity = self.findClosestOtherEntity()
            if closestEntity and self.isInSightRange(closestEntity):
                self.target = closestEntity
                self.moveToOrAttack(self.target)
                return
            self.moveRandomly()
            self.timeFromLastAttack += self.clock.get_time()
            return

        if not self.isInSightRange(self.target):
            self.target = None
            self.destinationPosition = None
            self.timeFromLastAttack += self.clock.get_time()
            return

        self.moveToOrAttack(self.target)
