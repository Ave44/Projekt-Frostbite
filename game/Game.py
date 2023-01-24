import sys

from pygame import mixer
from pygame.math import Vector2

from config import *
from game.Menu import Menu
from game.entities.Player import Player
from game.InputManager import InputManager
from game.tiles.CollidableTile import CollidableTile
from game.tiles.Tile import Tile
from game.ui.inventory.Inventory import Inventory
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup
from game.items.Item import Item
from game.items.Sword import Sword
from gameInitialization.GenerateMap import generateMap, loadImages


class Game:
    def __init__(self, screen, saveData):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.visibleSprites = CameraSpriteGroup()
        self.obstacleSprites = pygame.sprite.Group()
        self.UiSprites = UiSpriteGroup()

        # self.createMap(saveData["world_map"])
        self.createMap(generateMap(31))

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
        sword2 = Sword(self.visibleSprites, Vector2(200, 200))
        self.player.inventory.addItem(sword, self.player.selectedItem)
        unknownItem = Item(self.visibleSprites, Vector2(200, 200))
        self.player.inventory.addItem(unknownItem, self.player.selectedItem)

        self.InputManager = InputManager(self.player, self.UiSprites, self.visibleSprites)
        self.menu = Menu(screen, self.play, self.options, self.quitGame)

    # later will be replaced with LoadGame(savefile) class
    def createMap(self, worldMap):
        # for rowIndex, row in enumerate(worldMap):
        #    for columnIndex, column in enumerate(row):
        #        x = columnIndex * TILE_SIZE
        #        y = rowIndex * TILE_SIZE
        #        if column == 0:
        #            self.visibleSprites.addTile(CollidableTile((x, y), self.obstacleSprites))
        #        else:
        #            self.visibleSprites.addTile(Tile((x, y)))
        dictOfImages = loadImages()
        for rowIndex, row in enumerate(worldMap):
            for columnIndex, column in enumerate(row):
                for biome in dictOfImages:
                    x = columnIndex * TILE_SIZE
                    y = rowIndex * TILE_SIZE
                    if dictOfImages[biome]["collidable"].get(column) is not None:
                        tile = CollidableTile((x, y), dictOfImages[biome]["collidable"][column], self.obstacleSprites)
                        self.visibleSprites.addTile(tile)
                    elif dictOfImages[biome]["walkable"].get(column) is not None:
                        tile = Tile((x, y), dictOfImages[biome]["walkable"][column])
                        self.visibleSprites.addTile(tile)

    def debug(self, text):
        font = pygame.font.SysFont(None, 24)
        img = font.render(text, True, (255, 255, 255))
        self.screen.blit(img, (10, 10))

    def quitGame(self) -> None:
        pygame.quit()
        sys.exit()

    def mainMenu(self) -> None:
        self.changeMusicTheme(MENU_THEME)
        self.menu.mainMenu()

    def options(self) -> None:
        pass

    def changeMusicTheme(self, theme):
        mixer.music.load(theme)
        mixer.music.play(-1)
        mixer.music.set_volume(MAIN_THEME_VOLUME)

    def play(self):
        self.changeMusicTheme(HAPPY_THEME)
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
