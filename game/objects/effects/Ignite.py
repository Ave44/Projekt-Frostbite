from pygame.time import Clock

from game.objects.Object import Object
from game.objects.effects.Effect import Effect


class Ignite(Effect):
    def __init__(self, amountOfTicks: int, damagePerTick: int, object: Object, clock: Clock):
        super().__init__(amountOfTicks, object, clock)
        self.damagePerTick = damagePerTick

    def canApply(self) -> bool:
        return self.object.isFlammable

    def action(self) -> None:
        self.object.getDamage(self.damagePerTick)
