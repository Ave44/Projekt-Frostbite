import pygame
from pygame.math import Vector2
from pygame import Rect

from Config import Config
from constants import SLOT_SIZE
from game.ui.inventory.Inventory import Inventory
from game.ui.inventory.slot.SelectedItem import SelectedItem
from game.DayNightClock import DayNightClock


class UiSpriteGroup(pygame.sprite.Group):
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.displaySurface = pygame.display.get_surface()
        self.inventory = Inventory
        self.selectedItem = SelectedItem
        self.clock = DayNightClock
        self.clockRect = Rect
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

        self.displaySurface.blit(self.clock.background, self.clockRect)
        self.clock.drawHand(self.displaySurface, self.clockRect)

    def setClock(self, clock: DayNightClock):
        self.clock = clock
        self.clockRect = Rect(self.config.WINDOW_WIDTH - self.clock.radius * 2 - 10, 10, clock.radius * 2, clock.radius * 2)