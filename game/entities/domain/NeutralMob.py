from abc import ABC

from game.entities.domain.AggressiveMob import AggressiveMob
from game.entities.domain.State import State


class NeutralMob(AggressiveMob, ABC):
    def localUpdate(self):
        if not self.target and self.state != State.DAMAGED:
            return

        AggressiveMob.localUpdate(self)
