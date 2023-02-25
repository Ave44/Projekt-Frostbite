from pygame.time import Clock

from game.objects.Object import Object
from game.objects.effects.Effect import Effect


class Repair(Effect):
    def __init__(self, amountOfTicks: int, healPerTick: int, object: Object, clock: Clock):
        super().__init__(amountOfTicks, object, clock)
        self.healPerTick = healPerTick

    def canApply(self) -> bool:
        return self.object.isFlammable

    def action(self) -> None:
        self.object.heal(self.healPerTick)
