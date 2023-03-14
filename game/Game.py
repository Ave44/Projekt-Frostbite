import random

from pygame import mixer
from pygame.math import Vector2

from config import *
from game.entities.Enemy import Enemy
from game.entities.Player import Player
from game.InputManager import InputManager
from game.objects.trees.SmallTree import SmallTree
from game.objects.trees.TreeSapling import TreeSapling
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

        self.map = self.createMap(512)

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
        TreeSapling(self.visibleSprites, self.obstacleSprites, self.player.rect.midbottom, self.clock)
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
        if self.tick == 1000:
            self.spawnEnemy()
        if self.tick == 2000:
            self.tick = 0
            self.spawnEnemy()
            self.player.heal(20)

    def spawnEnemy(self):
        randomFactor = random.choice([Vector2(1, 1), Vector2(-1, 1), Vector2(1, -1), Vector2(-1, -1)])
        offset = Vector2(random.randint(128, 512) * randomFactor.x, random.randint(128, 512) * randomFactor.y)
        position = [self.player.rect.centerx + offset.x, self.player.rect.centery + offset.y]
        Enemy(self.visibleSprites, self.obstacleSprites, {
            "speed": 3,
            "maxHealth": 60,
            "currentHealth": 60,
            "damage": 20,
            "sightRange": 400,
            "attackRange": 20,
            "position_center": position,
            "path_to_image_up": "./graphics/entities/enemy/enemy.png",
            "path_to_image_down": "./graphics/entities/enemy/enemy.png",
            "path_to_image_left": "./graphics/entities/enemy/enemy.png",
            "path_to_image_right": "./graphics/entities/enemy/enemy.png",

            "path_to_image_up_heal": "./graphics/entities/enemy/enemy.png",
            "path_to_image_down_heal": "./graphics/entities/enemy/enemy.png",
            "path_to_image_left_heal": "./graphics/entities/enemy/enemy.png",
            "path_to_image_right_heal": "./graphics/entities/enemy/enemy.png",

            "path_to_image_up_damage": "./graphics/entities/enemy/enemy.png",
            "path_to_image_down_damage": "./graphics/entities/enemy/enemy.png",
            "path_to_image_left_damage": "./graphics/entities/enemy/enemy.png",
            "path_to_image_right_damage": "./graphics/entities/enemy/enemy.png",
        }, self.clock)

    def changeMusicTheme(self, theme):
        mixer.music.load(theme)
        mixer.music.play(-1)
        mixer.music.set_volume(MAIN_THEME_VOLUME)

    def entitiesUpdate(self):
        for entity in self.visibleSprites.entities:
            if type(entity) is Enemy:
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
