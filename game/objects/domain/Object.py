from abc import ABC, abstractmethod

from pygame.math import Vector2
from pygame.sprite import Group, Sprite
from pygame.surface import Surface

from typing import Type
from game.items.domain.Tool import Tool


class Object(ABC, Sprite):
    def __init__(self, visibleGroup: Group,
                 midBottom: Vector2, durability: int,
                 toolType: Type,
                 image: Surface):

        Sprite.__init__(self, visibleGroup)
        self.visibleGroup = visibleGroup

        self.image = image
        self.rect = self.image.get_rect(midbottom=midBottom)

        self.maxDurability = durability
        self.currentDurability = durability
        self.toolType = toolType

    @abstractmethod
    def drop(self) -> None:
        pass

    def onLeftClickAction(self, player) -> None:
        pass

    def canInteract(self, tool: Tool) -> bool:
        return isinstance(tool, self.toolType)

    def repair(self, amount: int) -> None:
        if self.currentDurability != self.maxDurability:
            self.currentDurability = min(self.currentDurability + amount, self.maxDurability)

    def getDamage(self, amount: int) -> None:
        if self.currentDurability - amount <= 0:
            self.destroy()
        else:
            self.currentDurability -= amount

    def destroy(self) -> None:
        self.remove(*self.groups())
        self.drop()
