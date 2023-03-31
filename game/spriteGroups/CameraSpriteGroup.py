import pygame
from pygame import Surface
from pygame.math import Vector2

from config import WINDOW_HEIGHT, WINDOW_WIDTH, TILES_ON_SCREEN_HEIGHT, TILES_ON_SCREEN_WIDTH, TILE_SIZE
from game.lightning.Glowing import Glowing
from game.spriteGroups.EntitiesGroup import EntitiesGroup


class CameraSpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.halfWindowHeight = WINDOW_HEIGHT // 2
        self.halfWindowWidth = WINDOW_WIDTH // 2
        self.offset = Vector2()
        self.map = []
        self.entities = EntitiesGroup()
        self.sunlight: Surface | None = None
        # self.radiuses = []

    def customDraw(self, center):
        self.offset.x = center.x - self.halfWindowWidth
        self.offset.y = center.y - self.halfWindowHeight
        self.drawTiles()

        for sprite in self.entities.sprites():
            self.drawSprite(sprite)
            if isinstance(sprite, Glowing) and self.sunlight.get_alpha():
                self.drawLightning(sprite)

        for sprite in self.sprites():
            self.drawSprite(sprite)
            if isinstance(sprite, Glowing) and self.sunlight.get_alpha():
                self.drawLightning(sprite)

        if self.sunlight:
            self.displaySurface.blit(self.sunlight, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Displaying radiuses is causing a lot of lag use only to debug
        # for radius in self.radiuses:
        #     self.drawRadius(radius["radius"], radius["position"], radius["color"])
        self.radiuses = []

    def drawSprite(self, sprite):
        spritePosition = sprite.rect.topleft - self.offset
        self.displaySurface.blit(sprite.image, spritePosition)

    def drawTiles(self):
        xGap = int(self.offset.x / TILE_SIZE)
        yGap = int(self.offset.y / TILE_SIZE)
        for y in range(TILES_ON_SCREEN_HEIGHT):
            for x in range(TILES_ON_SCREEN_WIDTH):
                if x + xGap < len(self.map) and y + yGap < len(self.map):
                    tile = self.map[y + yGap][x + xGap]
                    self.drawSprite(tile)

    def drawLightning(self, sprite: Glowing):
        halfLightSize = sprite.light.get_size()[0] // 2
        lightPosition = sprite.rect.center - self.offset - Vector2(halfLightSize, halfLightSize)
        self.sunlight.blit(sprite.light, lightPosition)

    # def addRadius(self, radius, position, color):
    #     self.radiuses.append({"radius": radius, "position": position, "color": color})

    # def drawRadius(self, radius, position, color):
    #     circleSurface = pygame.Surface((radius * 2, radius * 2))
    #     circleSurface.set_colorkey((0, 0, 0))
    #     circleSurface.set_alpha(80)
    #     pygame.draw.circle(circleSurface, color, (radius, radius), radius)
    #     self.displaySurface.blit(circleSurface, (position[0] - radius - self.offset.x, position[1] - radius - self.offset.y))
