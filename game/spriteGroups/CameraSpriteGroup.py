import pygame
from pygame.math import Vector2
from game.spriteGroups.EntitiesGroup import EntitiesGroup
import numpy as np

from config import WINDOW_HEIGHT, WINDOW_WIDTH, TILES_ON_SCREEN_HEIGHT, TILES_ON_SCREEN_WIDTH, TILE_SIZE


class CameraSpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.halfWindowHeight = WINDOW_HEIGHT // 2
        self.halfWindowWidth = WINDOW_WIDTH // 2
        self.offset = Vector2()
        self.tiles = []
        self.map = []
        self.chunks = []
        self.entities = EntitiesGroup()
        # self.radiuses = []

    def customDraw(self, center):
        self.offset.x = center.x - self.halfWindowWidth
        self.offset.y = center.y - self.halfWindowHeight
        # self.drawTiles()
        self.drawTiles2()

        for sprite in self.entities.sprites():
            spritePosition = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, spritePosition)

        for sprite in self.sprites():
            spritePosition = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, spritePosition)

        # Displaying radiuses is causing a lot of lag use only to debug
        # for radius in self.radiuses:
        #     self.drawRadius(radius["radius"], radius["position"], radius["color"])
        self.radiuses = []


    def addTile(self, tile):
        self.tiles.append(tile)

    def drawTiles(self):
        xGap = int(self.offset.x / TILE_SIZE)
        yGap = int(self.offset.y / TILE_SIZE)
        for y in range(TILES_ON_SCREEN_HEIGHT):
            for x in range(TILES_ON_SCREEN_WIDTH):
                if x + xGap < len(self.map) and y + yGap < len(self.map):
                    tile = self.map[y + yGap][x + xGap]
                    spritePosition = tile.rect.topleft - self.offset
                    self.displaySurface.blit(tile.image, spritePosition)

    def drawTiles2(self):
        chunkWidth = self.chunks[0][0].get_width()
        chunkHeight = self.chunks[0][0].get_height()
        
        xIndex = int(self.offset.x / chunkWidth)
        yIndex = int(self.offset.y / chunkHeight)
        chunksWidth = len(self.chunks[0])
        chunksHeight = len(self.chunks)
        for y in range(2):
            yPos = (yIndex + y) * chunkHeight - self.offset.y
            for x in range(2):
                xPos = (xIndex + x) * chunkWidth - self.offset.x
                chunkIndexX = xIndex + x
                chunkIndexY = yIndex + y
                if chunkIndexY < chunksHeight and chunkIndexX < chunksWidth: 
                    chunk = self.chunks[chunkIndexY][chunkIndexX]
                    chunkPosition = (xPos, yPos)
                    self.displaySurface.blit(chunk, chunkPosition)

    def addRadius(self, radius, position, color):
        self.radiuses.append({"radius": radius, "position": position, "color": color})

    def drawRadius(self, radius, position, color):
        circleSurface = pygame.Surface((radius*2, radius*2))
        circleSurface.set_colorkey((0,0,0))
        circleSurface.set_alpha(80)
        pygame.draw.circle(circleSurface, color, (radius, radius), radius)
        self.displaySurface.blit(circleSurface, (position[0] - radius - self.offset.x, position[1] - radius - self.offset.y))