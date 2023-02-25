from pygame.time import Clock

from game.objects.Object import Object
from game.objects.effects.Effect import Effect


class IgniteAndRepair(Effect):
    def __init__(self, amountOfTicks: int, damagePerTick: int, healPerTick: int, object: Object, clock: Clock):
        super().__init__(amountOfTicks, object, clock)
        self.damagePerTick = damagePerTick
        self.healPerTick = healPerTick

    def canApply(self) -> bool:
        return self.object.isFlammable

    def action(self) -> None:
        if self.amountOfTicks % 2 == 0:
            self.object.getDamage(self.damagePerTick)
        else:
            self.object.heal(self.healPerTick)
