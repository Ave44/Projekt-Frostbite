import random
import time

import pygame
from pygame import mixer, Surface
from pygame.math import Vector2
from pygame.time import Clock

from Config import Config
from constants import TILE_SIZE, HAPPY_THEME, FONT_MENU_COLOR
from game.DayCycle import DayCycle
from game.InputManager import InputManager
from game.LoadedImages import LoadedImages
from game.LoadedSounds import LoadedSounds
from game.entities.Boar import Boar
from game.entities.Bomb import Bomb
from game.entities.Deer import Deer
from game.entities.Player import Player
from game.entities.Rabbit import Rabbit
from game.items.Sword import Sword
from game.items.domain.Item import Item
from game.objects.GoblinHideout import GoblinHideout
from game.entities.GoblinChampion import GoblinChampion

from game.objects.Grass import Grass
from game.objects.RabbitHole import RabbitHole
from game.objects.Rock import Rock
from game.objects.trees.LargeTree import LargeTree
from game.objects.trees.MediumTree import MediumTree
from game.objects.trees.SmallTree import SmallTree
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup
from game.items.domain.Item import Item
from game.items.Sword import Sword
from game.items.StoneAxe import StoneAxe
from game.items.StonePickaxe import StonePickaxe
from game.items.WoodenArmor import WoodenArmor
from game.items.LeatherArmor import LeatherArmor
from game.tiles.Tile import Tile
from game.weathers.WeatherController import WeatherController
from gameInitialization.GenerateMap import generateMap


class Game:
    def __init__(self, screen: Surface, config: Config, saveData):
        self.config = config
        self.screen = screen
        self.clock = Clock()

        self.loadedImages = LoadedImages()
        self.loadedSounds = LoadedSounds()

        self.visibleSprites = CameraSpriteGroup(config)
        self.obstacleSprites = ObstacleSprites(config)
        self.UiSprites = UiSpriteGroup(config, self.visibleSprites, self.loadedImages)

        self.tick = 0

        self.map = self.createMap(100)
        self.dayCycle = DayCycle(1, 60000, 2 * 64 * 1000, self.clock, config, self.UiSprites, self.visibleSprites)

        self.player = Player(self.visibleSprites,
                             self.obstacleSprites,
                             self.UiSprites,
                             self.loadedImages,
                             self.loadedSounds,
                             config,
                             self.clock,
                             Vector2(0, 0),
                             currHunger=100,
                             hungerDecreasePerSecond=50)

        self.weatherController = WeatherController(self.loadedImages, self.clock, config, Vector2(self.player.rect.center))
        self.visibleSprites.weatherController = self.weatherController

        if not self.map[self.player.rect.centerx // TILE_SIZE][self.player.rect.centery // TILE_SIZE]['walkable']:
            for y in range(len(self.map)):
                for x in range(len(self.map)):
                    if self.map[y][x]['walkable']:
                        self.player.rect.centerx = x * TILE_SIZE + TILE_SIZE // 2
                        self.player.rect.centery = y * TILE_SIZE + TILE_SIZE // 2
                        self.player.colliderRect.midbottom = self.player.rect.midbottom
                        break
                else:
                    continue
                break

        GoblinChampion(self.visibleSprites, self.obstacleSprites, self.loadedImages, self.loadedSounds, self.clock, self.player.rect.midbottom)
        Deer(self.visibleSprites, self.obstacleSprites, self.loadedImages, self.loadedSounds, self.clock, self.player.rect.midbottom)
        Rabbit(self.visibleSprites, self.obstacleSprites, self.loadedImages, self.loadedSounds, self.clock, self.player.rect.midbottom)
        Boar(self.visibleSprites, self.obstacleSprites, self.loadedImages, self.loadedSounds, self.clock, self.player.rect.midbottom)
        self.rabbitHole = RabbitHole(self.visibleSprites, self.obstacleSprites, self.loadedImages, self.loadedSounds, self.player.rect.midbottom, self.clock)
        # self.goblinHideout = GoblinHideout(self.visibleSprites, self.obstacleSprites, self.loadedImages, self.loadedSounds, self.player.rect.midbottom, self.clock)

        sword = Sword(self.visibleSprites, Vector2(200, 200), self.loadedImages)
        self.player.inventory.addItem(sword, self.player.selectedItem)
        self.player.inventory.addItem(StoneAxe(self.visibleSprites, (0, 0), self.loadedImages), self.player.selectedItem)
        self.player.inventory.addItem(StonePickaxe(self.visibleSprites, (0, 0), self.loadedImages), self.player.selectedItem)
        self.player.inventory.addItem(Item(self.visibleSprites, (0, 0), self.loadedImages), self.player.selectedItem)
        self.player.inventory.addItem(WoodenArmor(self.visibleSprites, (0, 0), self.loadedImages), self.player.selectedItem)
        self.player.inventory.addItem(LeatherArmor(self.visibleSprites, (0, 0), self.loadedImages), self.player.selectedItem)

        self.inputManager = InputManager(self.player, self.UiSprites, self.visibleSprites)

    def generateMapLoadingScreen(self, information: str) -> None:
        self.screen.fill((0, 0, 0))
        infoText = self.config.fontBig.render(information, True, FONT_MENU_COLOR)
        infoRect = infoText.get_rect(center=(0.5 * self.config.WINDOW_WIDTH, 0.5 * self.config.WINDOW_HEIGHT))
        self.screen.blit(infoText, infoRect)
        pygame.display.flip()

    # later will be replaced with LoadGame(savefile) class
    def createMap(self, mapSize):
        map, objects = generateMap(mapSize, self.generateMapLoadingScreen)
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
        img = self.config.fontTiny.render(text, True, (255, 255, 255))
        self.screen.blit(img, (10, 10))

    def handleTick(self):
        self.tick = self.tick + 1
        if self.tick == 1000:
            self.spawnBomb()
            self.rabbitHole.onNewDay()
        #            self.goblinHideout.onNewDay()
        if self.tick == 2000:
            self.tick = 0
            self.spawnBomb()
            self.rabbitHole.onEvening()
            self.player.heal(20)

    def spawnBomb(self):
        randomFactor = random.choice([Vector2(1, 1), Vector2(-1, 1), Vector2(1, -1), Vector2(-1, -1)])
        offset = Vector2(random.randint(128, 512) * randomFactor.x, random.randint(128, 512) * randomFactor.y)
        position = Vector2(self.player.rect.centerx + offset.x, self.player.rect.centery + offset.y)
        Bomb(self.visibleSprites, self.obstacleSprites, self.loadedImages.bomb, self.loadedSounds.bomb, position, self.clock)

    def changeMusicTheme(self, theme):
        mixer.music.load(theme)
        mixer.music.play(-1)

    def play(self):
        self.changeMusicTheme(HAPPY_THEME)
        while True:
            self.inputManager.handleInput()
            self.dayCycle.updateDayCycle()
            self.visibleSprites.update()
            self.handleTick()
            playerCenter = Vector2(self.player.rect.center)
            self.weatherController.update(playerCenter)
            self.visibleSprites.customDraw(playerCenter)

            self.UiSprites.customDraw()

            # method for debugging values by writing them on screen
            # text = f"mx:{pygame.mouse.get_pos()[0]}, my:{pygame.mouse.get_pos()[1]}"
            text = f"x:{self.player.rect.centerx}, y:{self.player.rect.centery}, {self.clock.get_fps()}"
            self.debug(text)

            pygame.display.update()
            self.clock.tick()
