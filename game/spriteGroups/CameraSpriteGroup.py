import pygame
from pygame.math import Vector2
from game.spriteGroups.EntitiesGroup import EntitiesGroup

from config import WINDOW_HEIGHT, WINDOW_WIDTH


class CameraSpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.halfWindowHeight = WINDOW_HEIGHT // 2
        self.halfWindowWidth = WINDOW_WIDTH // 2
        self.offset = Vector2()
        self.tiles = []
        self.entities = EntitiesGroup()
        self.radiuses = []

    def customDraw(self, center):
        self.offset.x = center.x - self.halfWindowWidth
        self.offset.y = center.y - self.halfWindowHeight

        for tile in self.tiles:
            spritePosition = tile.rect.topleft - self.offset
            self.displaySurface.blit(tile.image, spritePosition)

        for sprite in self.entities.sprites():
            spritePosition = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, spritePosition)

        for sprite in self.sprites():
            spritePosition = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, spritePosition)

        for radius in self.radiuses:
            self.drawRadius(radius["radius"], radius["position"])
        self.radiuses = []


    def addTile(self, tile):
        self.tiles.append(tile)

    def addRadius(self, radius, position):
        self.radiuses.append({"radius": radius, "position": position})

    def drawRadius(self, radius, position):
        circleSurface = pygame.Surface((radius*2, radius*2))
        circleSurface.set_colorkey((0,0,0))
        circleSurface.set_alpha(80)
        pygame.draw.circle(circleSurface, (100, 100, 100), (radius, radius), radius)
        self.displaySurface.blit(circleSurface, (position[0] - radius - self.offset.x, position[1] - radius - self.offset.y))