from pygame.sprite import AbstractGroup

from config import *
from game.InputManager import InputManager
from entities.Player import Player
from game.Tile import Tile
from spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from spriteGroups.UiSpriteGroup import UiSpriteGroup
from ui.inventory.items.Item import Item
from ui.inventory.items.Sword import Sword
from game.ui.inventory.Inventory import Inventory


class Game:
    def __init__(self, screen, saveData):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.visibleSprites = CameraSpriteGroup()
        self.obstacleSprites = pygame.sprite.Group()
        self.UiSprites = UiSpriteGroup()

        self.createMap(saveData["world_map"])

        inventoryPosition = pygame.math.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 60)
        inventory = Inventory(self.UiSprites, 2, 12, inventoryPosition)
        inventory.open()

        self.player = Player(self.visibleSprites, self.obstacleSprites, saveData["player_data"], inventory)

        self.UiSprites.inventory = inventory
        self.UiSprites.selectedItem = self.player.selectedItem

        sword = Sword(self.visibleSprites, pygame.math.Vector2(200, 200))
        self.player.inventory.addItem(sword, self.player.selectedItem)
        unknownItem = Item(self.visibleSprites, pygame.math.Vector2(200, 200))
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
                self.visibleSprites.add_tile(tile)

    def debug(self, text):
        font = pygame.font.SysFont(None, 24)
        img = font.render(text, True, (255, 255, 255))
        self.screen.blit(img, (10, 10))

    def play(self):
        while True:
            self.InputManager.handleInput()

            self.visibleSprites.update()
            self.visibleSprites.custom_draw(pygame.math.Vector2(self.player.rect.center))

            self.UiSprites.custom_draw()

            # method for debugging values by writing them on screen
            text = f"mx:{pygame.mouse.get_pos()[0]}, my:{pygame.mouse.get_pos()[1]}"
            self.debug(text)

            pygame.display.update()
            self.clock.tick(FPS)
