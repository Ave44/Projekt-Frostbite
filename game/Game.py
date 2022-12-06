from pygame.math import Vector2
from pygame.sprite import AbstractGroup

from config import *
from entities.Player import Player
from game.InputManager import InputManager
from game.Tile import Tile
from game.ui.inventory.Inventory import Inventory
from spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from spriteGroups.UiSpriteGroup import UiSpriteGroup
from items.Item import Item
from items.Sword import Sword


class Game:
    def __init__(self, screen, saveData):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.visibleSprites = CameraSpriteGroup()
        self.obstacleSprites = pygame.sprite.Group()
        self.UiSprites = UiSpriteGroup()

        self.createMap(saveData["world_map"])

        inventoryPosition = Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 60)
        inventory = Inventory(self.UiSprites, 2, 12, inventoryPosition)
        inventory.open()

        self.player = Player(self.visibleSprites,
                             self.obstacleSprites,
                             saveData["player_data"],
                             inventory)

        self.UiSprites.player = self.player
        self.UiSprites.inventory = inventory
        self.UiSprites.selectedItem = self.player.selectedItem

        sword = Sword(self.visibleSprites, Vector2(200, 200))
        self.player.inventory.addItem(sword, self.player.selectedItem)
        unknownItem = Item(self.visibleSprites, Vector2(200, 200))
        self.player.inventory.addItem(unknownItem, self.player.selectedItem)

        self.InputManager = InputManager(self.player, self.UiSprites, self.visibleSprites)

    # later will be replaced with LoadGame(savefile) class
    def createMap(self, worldMap):
        for rowIndex, row in enumerate(worldMap):
            for columnIndex, column in enumerate(row):
                x = columnIndex * TILE_SIZE
                y = rowIndex * TILE_SIZE
                if column == 0:
                    tile = Tile((x, y), column, self.obstacleSprites)
                else:
                    tile = Tile((x, y), column, AbstractGroup())
                self.visibleSprites.addTile(tile)

    def debug(self, text):
        font = pygame.font.SysFont(None, 24)
        img = font.render(text, True, (255, 255, 255))
        self.screen.blit(img, (10, 10))

    def play(self):
        while True:
            self.InputManager.handleInput()

            self.visibleSprites.update()
            self.visibleSprites.customDraw(Vector2(self.player.rect.center))

            self.UiSprites.customDraw()

            # method for debugging values by writing them on screen
            text = f"mx:{pygame.mouse.get_pos()[0]}, my:{pygame.mouse.get_pos()[1]}"
            self.debug(text)

            pygame.display.update()
            self.clock.tick(FPS)
