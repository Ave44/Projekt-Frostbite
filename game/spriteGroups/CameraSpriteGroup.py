import pygame
from pygame.math import Vector2

from config import WINDOW_HEIGHT, WINDOW_WIDTH
from game.entities.Enemy import Enemy
from game.entities.Player import Player


class CameraSpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.halfWindowHeight = WINDOW_HEIGHT // 2
        self.halfWindowWidth = WINDOW_WIDTH // 2
        self.offset = Vector2()
        self.tiles = []
        self.entities = []

    def customDraw(self, center):
        self.displaySurface.fill('black') # possibly unecessary step
        self.offset.x = center.x - self.halfWindowWidth
        self.offset.y = center.y - self.halfWindowHeight

        for tile in self.tiles:
            spritePosition = tile.rect.topleft - self.offset
            self.displaySurface.blit(tile.image, spritePosition)

        for sprite in self.entities:
            spritePosition = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, spritePosition)

        for sprite in self.sprites():
            spritePosition = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, spritePosition)


    def addTile(self, tile):
        self.tiles.append(tile)
