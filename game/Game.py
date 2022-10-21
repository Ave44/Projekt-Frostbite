import pygame, sys
from config import *
from game.Player import Player
from game.Tile import Tile

class Game():
    def __init__(self, screen, saveData):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.visibleSprites = pygame.sprite.Group()
        self.obstacleSprites = pygame.sprite.Group()

        self.createMap(saveData["world_map"])
        self.player = Player(saveData["player_position"], [self.visibleSprites], self.obstacleSprites)

	
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

            self.visibleSprites.update()
            self.screen.fill('black')
            self.visibleSprites.draw(self.screen)

            pygame.display.update()
            self.clock.tick(FPS)
