import pygame
from pygame.math import Vector2

from constants import SLOT_SIZE
from game.ui.inventory.Inventory import Inventory
from game.ui.inventory.slot.SelectedItem import SelectedItem


class UiSpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.inventory = Inventory
        self.selectedItem = SelectedItem
        self.player = None

    def customDraw(self):
        if self.inventory.isOpen:
            self.displaySurface.blit(self.inventory.image, self.inventory.rect)
            for slot in self.inventory.slotList:
                self.displaySurface.blit(slot.image, slot.rect)
                if slot.item:
                    self.displaySurface.blit(slot.item.icon, slot.rect)

        if not self.selectedItem.isEmpty():
            mousePos = Vector2(pygame.mouse.get_pos())
            displayPos = (mousePos.x - SLOT_SIZE / 2, mousePos.y - SLOT_SIZE / 2)
            self.displaySurface.blit(self.selectedItem.item.icon, displayPos)

        self.player.healthBar.draw(self.displaySurface)

        for sprite in self.sprites():
            self.displaySurface.blit(sprite.image, sprite.rect)
