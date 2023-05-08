from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.entities.Player import Player

import pygame
from pygame.math import Vector2
from pygame import Surface, Rect

from Config import Config
from constants import SLOT_SIZE, BG_COLOR, SLOT_GAP
from game.ui.inventory.Inventory import Inventory
from game.ui.inventory.slot.SelectedItem import SelectedItem
from game.ui.inventory.slot.Slot import Slot
from game.ui.DayNightClock import DayNightClock
from game.LoadedImages import LoadedImages
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class UiSpriteGroup(pygame.sprite.Group):
    def __init__(self, config: Config, cameraSpriteGroup: CameraSpriteGroup, loadedImages: LoadedImages):
        super().__init__()
        self.config = config
        self.displaySurface = pygame.display.get_surface()
        self.inventory = Inventory
        self.selectedItem = SelectedItem
        self.handSlot = Slot
        self.bodySlot = Slot
        self.equipmentBackground = Surface
        self.equipmentBackgroundRect = Rect
        self.clock = DayNightClock
        self.clockRect = Rect
        self.player: Player | None = None
        self.cameraSpriteGroup = cameraSpriteGroup
        self.pointer = loadedImages.pointer
        self.pointerOffset = Vector2(self.pointer.get_width() // 2, self.pointer.get_height() // 2, )

    def customDraw(self):
        if self.inventory.isOpen:
            if self.player.destinationPosition:
                pointerPosition = self.player.destinationPosition - self.cameraSpriteGroup.offset - self.pointerOffset
                self.displaySurface.blit(self.pointer, pointerPosition)

            if self.player.midDestinationPosition:
                pointerPosition = self.player.midDestinationPosition - self.cameraSpriteGroup.offset
                self.displaySurface.blit(self.pointer, pointerPosition)

            self.displaySurface.blit(self.inventory.image, self.inventory.rect)
            for slot in self.inventory.slotList:
                self.displaySurface.blit(slot.image, slot.rect)
                if slot.item:
                    self.displaySurface.blit(slot.item.icon, slot.rect)

            self.displaySurface.blit(self.equipmentBackground, self.equipmentBackgroundRect)
            self.displaySurface.blit(self.handSlot.image, self.handSlot.rect)
            if self.handSlot.item:
                self.displaySurface.blit(self.handSlot.item.icon, self.handSlot.rect)

            self.displaySurface.blit(self.bodySlot.image, self.bodySlot.rect)
            if self.bodySlot.item:
                self.displaySurface.blit(self.bodySlot.item.icon, self.bodySlot.rect)

        if not self.selectedItem.isEmpty():
            mousePos = Vector2(pygame.mouse.get_pos())
            displayPos = (mousePos.x - SLOT_SIZE / 2, mousePos.y - SLOT_SIZE / 2)
            self.displaySurface.blit(self.selectedItem.item.icon, displayPos)

        self.player.healthBar.draw(self.displaySurface)

        self.clock.draw(self.displaySurface, self.clockRect)

    def setClock(self, clock: DayNightClock):
        self.clock = clock
        self.clockRect = Rect(self.config.WINDOW_WIDTH - self.clock.radius * 2 - 10, 10, clock.radius * 2, clock.radius * 2)

    def setEquipmentSlots(self, handSlot, bodySlot):
        self.handSlot = handSlot
        self.bodySlot = bodySlot
        equipmentBackgroundSize = (SLOT_SIZE + SLOT_GAP * 3, SLOT_SIZE * 2 + SLOT_GAP * 3)
        self.equipmentBackground = Surface(equipmentBackgroundSize)
        self.equipmentBackground.fill(BG_COLOR)
        self.equipmentBackgroundRect = Rect((self.inventory.rect.topright), equipmentBackgroundSize)
