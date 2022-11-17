import pygame

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
        self.displaySurface.blit(self.inventory.image, self.inventory.rect)
        for slot in self.inventory.slotList:
            self.displaySurface.blit(slot.image, slot.rect.center)
            if slot.item:
                self.displaySurface.blit(slot.item.icon, slot.rect.center)

        if not self.selectedItem.isEmpty():
            mousePos = pygame.mouse.get_pos()
            self.displaySurface.blit(self.selectedItem.item.icon, mousePos)
