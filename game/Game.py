import pygame, sys
from config import *
from game.InputManager import InputManager
from game.Player import Player
from game.Tile import Tile
from game.CameraSpriteGroup import CameraSpriteGroup
from game.UiSpriteGroup import UiSpriteGroup
from game.item.Sword import Sword
from game.ui.SelectedItem import SelectedItem
from game.ui.inventory.Inventory import Inventory

class Game():
    def __init__(self, screen, saveData):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.visibleSprites = CameraSpriteGroup()
        self.obstacleSprites = pygame.sprite.Group()
        self.UiSprites = UiSpriteGroup()


        self.createMap(saveData["world_map"])

        inventoryPosition = pygame.math.Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT - 60)
        inventory = Inventory(self.UiSprites, 2, 12, inventoryPosition)
        self.UiSprites.inventory = inventory
        selectedItem = SelectedItem(None)
        self.UiSprites.selectedItem = selectedItem
        self.player = Player([self.visibleSprites], self.obstacleSprites, saveData["player_data"], inventory, selectedItem)

        sword = Sword([self.visibleSprites], pygame.math.Vector2(200, 200))
        self.player.inventory.addItem(sword, self.player.selectedItem)

        self.InputManager = InputManager(self.player, self.UiSprites)

	
    # later will be replaced with LoadGame(savefile) class
    def createMap(self, worldMap):
        for rowIndex, row in enumerate(worldMap):
            for columnIndex, column in enumerate(row):
                x = columnIndex * TILE_SIZE
                y = rowIndex * TILE_SIZE
                if column == 0:
                    Tile((x,y), column, [self.visibleSprites, self.obstacleSprites])
                else:
                    Tile((x,y), column, [self.visibleSprites])

    def debug(self, text):
        font = pygame.font.SysFont(None, 24)
        img = font.render(text, True, (255,255,255))
        self.screen.blit(img, (20, 20))


    def play(self):
        while True:
            self.InputManager.handleInput()

            self.visibleSprites.update()
            self.visibleSprites.customDraw(pygame.math.Vector2(self.player.rect.center))
            self.UiSprites.customDraw()

            # method for debuging values by writing them on screen
            text = f"mx:{pygame.mouse.get_pos()[0]}, my:{pygame.mouse.get_pos()[1]}"
            self.debug(text)

            pygame.display.update()
            self.clock.tick(FPS)
