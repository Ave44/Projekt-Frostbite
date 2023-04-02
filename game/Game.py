import random

import pygame
from pygame import mixer
from pygame.math import Vector2
from pygame.time import Clock

from Config import Config
from constants import TILE_SIZE, HAPPY_THEME
from game.InputManager import InputManager
from game.LoadedImages import LoadedImages
from game.entities.Boar import Boar
from game.entities.Bomb import Bomb
from game.entities.Deer import Deer
from game.entities.Player import Player
from game.entities.Rabbit import Rabbit
from game.items.Sword import Sword
from game.items.domain.Item import Item
from game.lightning.DayCycle import DayCycle
from game.objects.Grass import Grass
from game.objects.RabbitHole import RabbitHole
from game.objects.Rock import Rock
from game.objects.trees.LargeTree import LargeTree
from game.objects.trees.MediumTree import MediumTree
from game.objects.trees.SmallTree import SmallTree
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup
from game.tiles.Tile import Tile
from gameInitialization.GenerateMap import generateMap


class Game:
    def __init__(self, screen, config: Config, saveData):
        self.screen = screen
        self.clock = Clock()

        self.visibleSprites = CameraSpriteGroup(config)
        self.obstacleSprites = ObstacleSprites(config)
        self.UiSprites = UiSpriteGroup()

        self.dayCycle = DayCycle(self.visibleSprites, 50000, 60000, self.clock, config)
        self.tick = 0

        self.loadedImages = LoadedImages()
        self.map = self.createMap(100)

        self.player = Player(self.visibleSprites,
                             self.obstacleSprites,
                             self.UiSprites,
                             self.loadedImages.player,
                             config,
                             self.clock,
                             Vector2(0, 0))

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

        Deer(self.visibleSprites, self.obstacleSprites, self.loadedImages, self.clock, self.player.rect.midbottom)
        Rabbit(self.visibleSprites, self.obstacleSprites, self.loadedImages, self.clock, self.player.rect.midbottom)
        Boar(self.visibleSprites, self.obstacleSprites, self.loadedImages, self.clock, self.player.rect.midbottom)
        self.rabbitHole = RabbitHole(self.visibleSprites, self.obstacleSprites, self.loadedImages,
                                     self.player.rect.midbottom, self.clock)
        sword = Sword(self.visibleSprites, Vector2(200, 200), self.loadedImages)
        unknownItem = Item(self.visibleSprites, Vector2(200, 200), self.loadedImages)
        self.player.inventory.addItem(sword, self.player.selectedItem)
        self.player.inventory.addItem(unknownItem, self.player.selectedItem)

        self.inputManager = InputManager(self.player, self.UiSprites, self.visibleSprites)

    # later will be replaced with LoadGame(savefile) class
    def createMap(self, mapSize):
        map, objects = generateMap(mapSize, print)
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
        self.createObjects(objects)
        return map

    def createObjects(self, objects: dict) -> None:
        self.loadTrees(objects['trees'])
        self.loadRocks(objects['rocks'])
        self.loadGrasses(objects['grasses'])

    def loadTrees(self, treesData: dict) -> None:
        for treeData in treesData:
            if treeData['growthStage'] == 1:
                SmallTree(self.visibleSprites, self.obstacleSprites, treeData['midBottom'], self.loadedImages,
                          self.clock, treeData['age'])
            elif treeData['growthStage'] == 2:
                MediumTree(self.visibleSprites, self.obstacleSprites, treeData['midBottom'], self.loadedImages,
                           self.clock, treeData['age'])
            else:
                LargeTree(self.visibleSprites, self.obstacleSprites, treeData['midBottom'], self.loadedImages,
                          self.clock, treeData['age'])

    def loadRocks(self, rocksData: dict) -> None:
        for rockData in rocksData:
            Rock(self.visibleSprites, self.obstacleSprites, rockData['midBottom'], self.loadedImages)

    def loadGrasses(self, grassesData: dict) -> None:
        for grassData in grassesData:
            Grass(self.visibleSprites, grassData['midBottom'], self.loadedImages, self.clock)

    def debug(self, text):
        font = pygame.font.SysFont(None, 24)
        img = font.render(text, True, (255, 255, 255))
        self.screen.blit(img, (10, 10))

    def handleTick(self):
        self.tick = self.tick + 1
        if self.tick == 1000:
            self.spawnBomb()
            self.rabbitHole.onNewDay()
        if self.tick == 2000:
            self.tick = 0
            self.spawnBomb()
            self.rabbitHole.onEvening()
            self.player.heal(20)

    def spawnBomb(self):
        randomFactor = random.choice([Vector2(1, 1), Vector2(-1, 1), Vector2(1, -1), Vector2(-1, -1)])
        offset = Vector2(random.randint(128, 512) * randomFactor.x, random.randint(128, 512) * randomFactor.y)
        position = Vector2(self.player.rect.centerx + offset.x, self.player.rect.centery + offset.y)
        Bomb(self.visibleSprites, self.obstacleSprites, self.loadedImages.bomb, position, self.clock)

    def changeMusicTheme(self, theme):
        mixer.music.load(theme)
        mixer.music.play(-1)

    def play(self):
        self.changeMusicTheme(HAPPY_THEME)
        while True:
            self.inputManager.handleInput()
            self.visibleSprites.update()
            self.handleTick()
            self.visibleSprites.customDraw(Vector2(self.player.rect.center))

            self.dayCycle.updateDayCycle()

            self.UiSprites.customDraw()

            # method for debugging values by writing them on screen
            # text = f"mx:{pygame.mouse.get_pos()[0]}, my:{pygame.mouse.get_pos()[1]}"
            text = f"x:{self.player.rect.centerx}, y:{self.player.rect.centery}, {self.clock.get_fps()}"
            self.debug(text)

            pygame.display.update()
            self.clock.tick()
