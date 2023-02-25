from abc import ABC, abstractmethod

from pygame.math import Vector2
from pygame.sprite import Group, Sprite
from pygame.surface import Surface
from pygame.time import Clock

from game.items.ToolType import ToolType


class Object(ABC, Sprite):
    from game.objects.effects import Effect

    def __init__(self, visibleGroup: Group,
                 obstaclesGroup: Group,
                 center: Vector2(), durability: int,
                 toolType: ToolType,
                 isFlammable: bool, clock: Clock,
                 imageNormal: Surface, imageDamage: Surface, imageHeal: Surface):
        from game.objects.effects.Effect import Effect

        super().__init__(visibleGroup, obstaclesGroup)
        self.visibleGroup = visibleGroup
        self.obstaclesGroup = obstaclesGroup

        self.imageNormal = imageNormal
        self.imageDamage = imageDamage
        self.imageHeal = imageHeal
        self.image = imageNormal
        self.rect = self.image.get_rect(center=center)

        self.maxDurability = durability
        self.currentDurability = durability
        self.timeFromLastDurabilityChange = 0
        self.toolType = toolType
        self.isFlammable = isFlammable
        self.clock = clock
        self.activeEffects: list[Effect] = []

    @abstractmethod
    def dropItem(self) -> None:
        pass

    def destroy(self) -> None:
        self.visibleGroup.remove(self)
        self.obstaclesGroup.remove(self)
        self.dropItem()

    def getDamage(self, amount: int) -> None:
        if self.currentDurability - amount <= 0:
            self.destroy()
        else:
            self.currentDurability -= amount
            self.image = self.imageDamage
            self.timeFromLastDurabilityChange = 0

    def canInteract(self, toolType: ToolType) -> bool:
        return toolType == self.toolType

    def heal(self, amount: int) -> None:
        if self.currentDurability != self.maxDurability:
            self.currentDurability = min(self.currentDurability + amount, self.maxDurability)
            self.image = self.imageHeal
            self.timeFromLastDurabilityChange = 0

    def addEffect(self, effect: Effect) -> None:
        filteredActiveEffects = list(filter(lambda x: (x.__class__ != effect.__class__), self.activeEffects))
        filteredActiveEffects.append(effect)
        self.activeEffects = filteredActiveEffects

    def executeEffect(self, effect: Effect) -> None:
        if not effect.amountOfTicks:
            self.activeEffects.remove(effect)
        else:
            effect.execute()

    def update(self) -> None:
        timeFromLastTick = self.clock.get_time()
        for effect in self.activeEffects:
            self.executeEffect(effect)

        if self.timeFromLastDurabilityChange >= 250 and not self.image == self.imageNormal:
            self.image = self.imageNormal
        else:
            self.timeFromLastDurabilityChange += timeFromLastTick
