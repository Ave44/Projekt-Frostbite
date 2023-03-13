from abc import ABC, abstractmethod

from pygame.math import Vector2
from pygame.sprite import Group, Sprite
from pygame.surface import Surface

from game.items.ToolType import ToolType


class Object(ABC, Sprite):

    def __init__(self, visibleGroup: Group,
                 obstaclesGroup: Group,
                 midBottom: Vector2(), durability: int,
                 toolType: ToolType,
                 image: Surface):

        super().__init__(visibleGroup, obstaclesGroup)
        self.visibleGroup = visibleGroup
        self.obstaclesGroup = obstaclesGroup

        self.image = image
        self.rect = self.image.get_rect(midbottom=midBottom)

        self.maxDurability = durability
        self.currentDurability = durability
        self.toolType = toolType

    @abstractmethod
    def dropItem(self) -> None:
        pass

    @abstractmethod
    def interact(self) -> None:
        pass

    def canInteract(self, toolType: ToolType) -> bool:
        return toolType == self.toolType

    def repair(self, amount: int) -> None:
        if self.currentDurability != self.maxDurability:
            self.currentDurability = min(self.currentDurability + amount, self.maxDurability)

    def getDamage(self, amount: int) -> None:
        if self.currentDurability - amount <= 0:
            self.destroy()
        else:
            self.currentDurability -= amount

    def destroy(self) -> None:
        self.visibleGroup.remove(self)
        self.obstaclesGroup.remove(self)
        self.dropItem()
