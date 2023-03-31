import pygame
from pygame.math import Vector2
from game.spriteGroups.EntitiesGroup import EntitiesGroup

from constants import TILE_SIZE
from Config import Config

class CameraSpriteGroup(pygame.sprite.Group):
    def __init__(self, config: Config):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.config = config
        self.halfWindowHeight = config.WINDOW_HEIGHT // 2
        self.halfWindowWidth = config.WINDOW_WIDTH // 2
        self.offset = Vector2()
        self.map = []
        self.entities = EntitiesGroup()
        # self.radiuses = []

    def customDraw(self, center):
        self.offset.x = center.x - self.halfWindowWidth
        self.offset.y = center.y - self.halfWindowHeight
        self.drawTiles(self.config)

        for sprite in self.entities.sprites():
            spritePosition = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, spritePosition)

        for sprite in self.sprites():
            spritePosition = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, spritePosition)

        # self.radiuses = []

    def drawTiles(self, config: Config):
        xGap = int(self.offset.x / TILE_SIZE)
        yGap = int(self.offset.y / TILE_SIZE)
        for y in range(config.TILES_ON_SCREEN_HEIGHT):
            for x in range(config.TILES_ON_SCREEN_WIDTH):
                if x + xGap < len(self.map) and y + yGap < len(self.map):
                    tile = self.map[y + yGap][x + xGap]
                    spritePosition = tile.rect.topleft - self.offset
                    self.displaySurface.blit(tile.image, spritePosition)

    def addRadius(self, radius, position, color):
        self.radiuses.append({"radius": radius, "position": position, "color": color})

    def drawRadius(self, radius, position, color):
        circleSurface = pygame.Surface((radius*2, radius*2))
        circleSurface.set_colorkey((0,0,0))
        circleSurface.set_alpha(80)
        pygame.draw.circle(circleSurface, color, (radius, radius), radius)
        self.displaySurface.blit(circleSurface, (position[0] - radius - self.offset.x, position[1] - radius - self.offset.y))