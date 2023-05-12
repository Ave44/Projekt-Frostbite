import pygame
from pygame import Surface
from pygame.sprite import Sprite, Group
from pygame.math import Vector2

from constants import TILE_SIZE, COLLIDER_COLOR
from Config import Config
from game.lightning.Glowing import Glowing
from game.spriteGroups.EntitiesGroup import EntitiesGroup
from game.spriteGroups.SavefileGroups import SavefileGroups
from game.weathers.WeatherController import WeatherController


class CameraSpriteGroup(Group):
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
        self.savefileGroups = SavefileGroups()
        self.nightMask: Surface | None = None
        self.weatherController: WeatherController | None = None
        self.showHitboxex = False


    def customDraw(self, center: Vector2):
        self.offset.x = center.x - self.halfWindowWidth
        self.offset.y = center.y - self.halfWindowHeight
        self.drawTiles()

        nightMaskBrightness = self.nightMask.get_at((0, 0))[0]

        for sprite in self.sprites():
            self.drawSprite(sprite)
            if isinstance(sprite, Glowing) and nightMaskBrightness != 255:
                self.drawLightning(sprite)
        
        if self.showHitboxex:
            self.drawColliders()

        if self.weatherController:
            self.weatherController.draw(self.displaySurface)

        if nightMaskBrightness != 255:
            self.displaySurface.blit(self.nightMask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def drawSprite(self, sprite: Sprite):
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

    def drawColliders(self):
        for sprite in self.sprites():
            if hasattr(sprite, 'colliderRect'):
                rectPosition = sprite.colliderRect.topleft - self.offset
                colliderImage = Surface((sprite.colliderRect.width, sprite.colliderRect.height))
                colliderImage.fill(COLLIDER_COLOR)
                self.displaySurface.blit(colliderImage, rectPosition)

    def toggleShowHitboxes(self):
        self.showHitboxex = not self.showHitboxex
