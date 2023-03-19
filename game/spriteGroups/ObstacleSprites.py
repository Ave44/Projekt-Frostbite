import pygame
from game.spriteGroups.EntitiesGroup import EntitiesGroup

from config import WINDOW_HEIGHT, WINDOW_WIDTH, TILE_SIZE


class ObstacleSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.halfWindowHeight = WINDOW_HEIGHT // 2
        self.halfWindowWidth = WINDOW_WIDTH // 2
        self.map = []
        self.entities = EntitiesGroup()

    def getNearbyTiles(self, center: tuple):
        xGap = int(center[0] / TILE_SIZE - 1)
        yGap = int(center[1] / TILE_SIZE - 1)
        tiles = []
        for y in range(3):
            for x in range(3):
                if x + xGap < len(self.map) and y + yGap < len(self.map):
                    tile = self.map[y + yGap][x + xGap]
                    if tile:
                        tiles.append(tile)
        return tiles
    
    def getObstacles(self, center):
        sprites = self.sprites()
        tiles = self.getNearbyTiles(center)
        return sprites + tiles