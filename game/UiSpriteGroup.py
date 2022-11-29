import pygame

from config import SLOTSIZE
from game.ui.Bar import Bar
from game.ui.SelectedItem import SelectedItem
from game.ui.inventory.Inventory import Inventory
from game.ui.inventory.Slot import Slot


class UiSpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.inventory = None | Inventory
        self.selectedItem = None | SelectedItem


    def customDraw(self):
        if self.inventory.isOpen:
            self.displaySurface.blit(self.inventory.image, self.inventory.rect)
            for slot in self.inventory.slotList:
                self.displaySurface.blit(slot.image, slot.rect)
                if slot.item:
                    self.displaySurface.blit(slot.item.icon, slot.rect)

        if not self.selectedItem.isEmpty():
            mousePos = pygame.math.Vector2(pygame.mouse.get_pos())
            displayPos = (mousePos.x - SLOTSIZE/2, mousePos.y - SLOTSIZE/2)
            self.displaySurface.blit(self.selectedItem.item.icon, displayPos)

        for sprite in self.sprites():
            if type(sprite) == Bar:
                sprite.draw(self.displaySurface)
