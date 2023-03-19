import random

from pygame import mixer
from pygame.math import Vector2

from config import *
from game.entities.Boar import Boar
from game.entities.Bomb import Bomb
from game.entities.Deer import Deer
from game.entities.domain.AggressiveMob import AggressiveMob
from game.entities.Player import Player
from game.InputManager import InputManager
from game.entities.Rabbit import Rabbit
from game.tiles.Tile import Tile
from game.ui.inventory.Inventory import Inventory
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup
from game.items.Item import Item
from game.items.Sword import Sword
from gameInitialization.GenerateMap import generateMap


class Game:
    def __init__(self, screen, saveData):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.visibleSprites = CameraSpriteGroup()
        self.obstacleSprites = ObstacleSprites()
        self.UiSprites = UiSpriteGroup()

        self.tick = 0

        self.map = self.createMap(100)

        inventoryPosition = Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 60)
        inventory = Inventory(self.UiSprites, 2, 12, inventoryPosition)
        inventory.open()

        self.player = Player(self.visibleSprites,
                             self.obstacleSprites,
                             saveData["player_data"],
                             inventory, self.clock)
        
        if not self.map[self.player.rect.centerx // TILE_SIZE][self.player.rect.centery // TILE_SIZE]['walkable']:
            for y in range(len(self.map)):
                for x in range(len(self.map)):
                    if self.map[y][x]['walkable']:
                        self.player.rect.centerx = x * TILE_SIZE + TILE_SIZE // 2
                        self.player.rect.centery = y * TILE_SIZE + TILE_SIZE // 2
                        break
                else:
                    continue
                break

        self.UiSprites.player = self.player
        self.UiSprites.inventory = inventory
        self.UiSprites.selectedItem = self.player.selectedItem

        sword = Sword(self.visibleSprites, Vector2(200, 200))
        Deer(self.visibleSprites, self.obstacleSprites, self.clock, self.player.rect.midbottom)
        Rabbit(self.visibleSprites, self.obstacleSprites, self.clock, self.player.rect.midbottom)
        Boar(self.visibleSprites, self.obstacleSprites, self.clock, self.player.rect.midbottom)
        self.player.inventory.addItem(sword, self.player.selectedItem)
        unknownItem = Item(self.visibleSprites, Vector2(200, 200))
        self.player.inventory.addItem(unknownItem, self.player.selectedItem)

        self.InputManager = InputManager(self.player, self.UiSprites, self.visibleSprites)

    # later will be replaced with LoadGame(savefile) class
    def createMap(self, mapSize):
        map = generateMap(mapSize)
        tilesMap = [[None for x in range(mapSize)] for y in range(mapSize)]
        obstaclesMap = [[None for x in range(mapSize)] for y in range(mapSize)]
        for y in range(len(map)):
            for x in range(len(map)):
                xPos = x * TILE_SIZE
                yPos = y * TILE_SIZE
                tile = Tile((xPos, yPos), map[y][x]["image"])
                tilesMap[y][x] = tile
                if not map[y][x]["walkable"]:
                    obstaclesMap[y][x] = tile
        self.visibleSprites.map = tilesMap
        self.obstacleSprites.map = obstaclesMap
        return map        

    def debug(self, text):
        font = pygame.font.SysFont(None, 24)
        img = font.render(text, True, (255, 255, 255))
        self.screen.blit(img, (10, 10))

    def handleTick(self):
        self.tick = self.tick + 1
        # if self.tick == 1000:
        #     self.spawnBomb()
        # if self.tick == 2000:
        #     self.tick = 0
        #     self.spawnBomb()
        #     self.player.heal(20)

    def spawnBomb(self):
        randomFactor = random.choice([Vector2(1, 1), Vector2(-1, 1), Vector2(1, -1), Vector2(-1, -1)])
        offset = Vector2(random.randint(128, 512) * randomFactor.x, random.randint(128, 512) * randomFactor.y)
        position = Vector2(self.player.rect.centerx + offset.x, self.player.rect.centery + offset.y)
        Bomb(self.visibleSprites, self.obstacleSprites, position, self.clock)

    def changeMusicTheme(self, theme):
        mixer.music.load(theme)
        mixer.music.play(-1)
        mixer.music.set_volume(MAIN_THEME_VOLUME)

    def entitiesUpdate(self):
        for entity in self.visibleSprites.entities:
            if type(entity) is AggressiveMob:
                entity.searchForTarget(self.visibleSprites.entities)

    def play(self):
        self.changeMusicTheme(HAPPY_THEME)
        while True:
            self.InputManager.handleInput()

            self.entitiesUpdate()

            self.visibleSprites.update()
            self.handleTick()
            self.visibleSprites.customDraw(Vector2(self.player.rect.center))

            self.UiSprites.customDraw()

            # method for debugging values by writing them on screen
            # text = f"mx:{pygame.mouse.get_pos()[0]}, my:{pygame.mouse.get_pos()[1]}"
            text = f"x:{self.player.rect.centerx}, y:{self.player.rect.centery}"
            self.debug(text)

            pygame.display.update()
            self.clock.tick(FPS)
