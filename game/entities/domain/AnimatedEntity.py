from __future__ import annotations
from abc import abstractmethod, ABC
from game.entities.domain.Entity import Entity

class AnimatedEntity(Entity, ABC):
    def __init__(self):
        Entity.__init__()

    #def update(self) -> None:
    #    self.localUpdate()
#
    #    timeFromLastTick = self.clock.get_time()
    #    for effect in self.activeEffects:
    #        effect.execute()
#
    #    if self.state != State.NORMAL:
    #        if self.timeFromLastHealthChange >= 250:
    #            self.state = State.NORMAL
    #        else:
    #            self.timeFromLastHealthChange += timeFromLastTick