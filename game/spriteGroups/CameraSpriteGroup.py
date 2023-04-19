import pygame
from pygame import Surface
from pygame.math import Vector2

from game.lightning.Glowing import Glowing
from constants import TILE_SIZE
from Config import Config
from game.spriteGroups.EntitiesGroup import EntitiesGroup


class CameraSpriteGroup(pygame.sprite.Group):
    def __init__(self, config: Config):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.halfWindowHeight = config.WINDOW_HEIGHT // 2
        self.halfWindowWidth = config.WINDOW_WIDTH // 2
        self.tilesOnScreenHeight = config.TILES_ON_SCREEN_HEIGHT
        self.tilesOnScreenWidth = config.TILES_ON_SCREEN_WIDTH
        self.offset = Vector2()
        self.map = []
        self.entities = EntitiesGroup()
        self.nightMask: Surface | None = None
        # self.radiuses = []

    def customDraw(self, center):
        self.offset.x = center.x - self.halfWindowWidth
        self.offset.y = center.y - self.halfWindowHeight
        self.drawTiles()

        nightMaskBrightness = self.nightMask.get_at((0, 0))[0]

        for sprite in self.entities.sprites():
            self.drawSprite(sprite)
            if isinstance(sprite, Glowing) and nightMaskBrightness != 255:
                self.drawLightning(sprite)

        for sprite in self.sprites():
            self.drawSprite(sprite)
            if isinstance(sprite, Glowing) and nightMaskBrightness != 255:
                self.drawLightning(sprite)

        if nightMaskBrightness != 255:
            self.displaySurface.blit(self.nightMask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # self.radiuses = []

    def drawSprite(self, sprite):
        spritePosition = sprite.rect.topleft - self.offset
        self.displaySurface.blit(sprite.image, spritePosition)

    def drawTiles(self):
        xGap = int(self.offset.x / TILE_SIZE)
        yGap = int(self.offset.y / TILE_SIZE)
        for y in range(self.tilesOnScreenHeight):
            for x in range(self.tilesOnScreenWidth):
                if x + xGap < len(self.map) and y + yGap < len(self.map):
                    tile = self.map[y + yGap][x + xGap]
                    self.drawSprite(tile)

    def drawLightning(self, sprite: Glowing):
        lightPosition = sprite.calculateTopLeftPosition() - self.offset
        self.nightMask.blit(sprite.lightImage, lightPosition)

    # def addRadius(self, radius, position, color):
    #     self.radiuses.append({"radius": radius, "position": position, "color": color})

    # def drawRadius(self, radius, position, color):
    #     circleSurface = pygame.Surface((radius * 2, radius * 2))
    #     circleSurface.set_colorkey((0, 0, 0))
    #     circleSurface.set_alpha(80)
    #     pygame.draw.circle(circleSurface, color, (radius, radius), radius)
    #     self.displaySurface.blit(circleSurface, (position[0] - radius - self.offset.x, position[1] - radius - self.offset.y))
