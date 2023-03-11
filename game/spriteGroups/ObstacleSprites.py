import pygame
from pygame.math import Vector2
from game.spriteGroups.EntitiesGroup import EntitiesGroup

from config import WINDOW_HEIGHT, WINDOW_WIDTH, TILE_SIZE


class CameraSpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.halfWindowHeight = WINDOW_HEIGHT // 2
        self.halfWindowWidth = WINDOW_WIDTH // 2
        self.offset = Vector2()
        self.map = []
        self.entities = EntitiesGroup()

    def getNearbyTiles(self, center: Vector2):
        self.offset.x = center.x - self.halfWindowWidth
        self.offset.y = center.y - self.halfWindowHeight

        xGap = int(self.offset.x / TILE_SIZE)
        yGap = int(self.offset.y / TILE_SIZE)
        tiles = []
        for y in range(3):
            for x in range(3):
                if x + xGap < len(self.map) and y + yGap < len(self.map):
                    tile = self.map[y + yGap][x + xGap]
                    tiles.append(tile)
        return tiles