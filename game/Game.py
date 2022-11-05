import pygame, sys
from config import *
from game.Player import Player
from game.Tile import Tile
from game.CameraSpriteGroup import CameraSpriteGroup

class Game():
    def __init__(self, screen, saveData):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.visibleSprites = CameraSpriteGroup()
        self.obstacleSprites = pygame.sprite.Group()

        self.createMap(saveData["world_map"])

        self.player = Player([self.visibleSprites], self.obstacleSprites, saveData["player_data"])

	
    # later will be replaced with LoadGame(savefile) class
    def createMap(self, worldMap):
        for rowIndex, row in enumerate(worldMap):
            for columnIndex, column in enumerate(row):
                x = columnIndex * TILESIZE
                y = rowIndex * TILESIZE
                if column == 0:
                    Tile((x,y), column, [self.visibleSprites, self.obstacleSprites])
                else:
                    Tile((x,y), column, [self.visibleSprites])


    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.player.inventory.handleOpening()

            self.visibleSprites.update()
            self.visibleSprites.customDraw(pygame.math.Vector2(self.player.rect.center))

            pygame.display.update()
            self.clock.tick(FPS)
