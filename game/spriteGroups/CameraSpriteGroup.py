import pygame
from pygame.math import Vector2

from config import WINDOW_HEIGHT, WINDOW_WIDTH
from game.ui.inventory.Slot import Slot
from ui.inventory.state.SelectedItem import SelectedItem


class CameraSpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.halfWindowHeight = WINDOW_HEIGHT // 2
        self.halfWindowWidth = WINDOW_WIDTH // 2
        self.offset = Vector2()
        self.tilesSprites = []

    def customDraw(self, center):
        self.displaySurface.fill('black')
        self.offset.x = center.x - self.halfWindowWidth
        self.offset.y = center.y - self.halfWindowHeight

        for tile in self.tilesSprites:
            spritePosition = tile.rect.topleft - self.offset
            self.displaySurface.blit(tile.image, spritePosition)

        for sprite in self.sprites():
            spritePosition = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, spritePosition)
            if type(sprite) == Slot or type(sprite) == SelectedItem:
                if not sprite.isEmpty():
                    self.displaySurface.blit(sprite.item.icon, spritePosition)

    def addTile(self, tile):
        self.tilesSprites.append(tile)
