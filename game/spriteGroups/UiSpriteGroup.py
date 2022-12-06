import pygame
from pygame.math import Vector2

from config import SLOTSIZE
from game.ui.inventory.Inventory import Inventory
from ui.inventory.slot.SelectedItem import SelectedItem


class UiSpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.inventory = None | Inventory
        self.selectedItem = None | SelectedItem
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
            displayPos = (mousePos.x - SLOTSIZE/2, mousePos.y - SLOTSIZE/2)
            self.displaySurface.blit(self.selectedItem.item.icon, displayPos)

        self.player.healthBar.draw(self.displaySurface)
