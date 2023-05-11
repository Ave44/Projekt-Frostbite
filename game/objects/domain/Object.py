from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.entities.Player import Player
    from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
    
from abc import ABC, abstractmethod

from pygame.math import Vector2
from pygame.sprite import Sprite
from pygame.surface import Surface

from typing import Type
from game.items.domain.Tool import Tool


class Object(ABC, Sprite):
    def __init__(self, visibleGroup: CameraSpriteGroup, midBottom: Vector2,
                 durability: int, toolType: Type,
                 image: Surface, currentDurability: int = None):

        Sprite.__init__(self, visibleGroup)
        savefileGroup = getattr(visibleGroup.savefileGroups, type(self).__name__)
        savefileGroup.add(self)
        self.visibleGroup = visibleGroup

        self.image = image
        self.rect = self.image.get_rect(midbottom=midBottom)

        self.maxDurability = durability
        self.currentDurability = currentDurability if currentDurability else durability
        self.toolType = toolType

    @abstractmethod
    def drop(self) -> None:
        pass

    def onLeftClickAction(self, player: Player) -> None:
        playerItem = player.handSlot.item
        if isinstance(playerItem, self.toolType):
            self.getDamage(playerItem.toolPower)
            player.handSlot.reduceItemDurability()

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

    def getSaveData(self) -> list:
        return [self.rect.midbottom, self.currentDurability]