import random
import inspect
from json import dump

import pygame
from pygame import mixer, Surface, Rect
from pygame.math import Vector2
from pygame.time import Clock

from Config import Config
from constants import TILE_SIZE, HAPPY_THEME, FONT_MENU_COLOR
from gameInitialization.GenerateMap import populateMapWithData
from game.DayCycle import DayCycle
from game.InputManager import InputManager
from game.LoadedImages import LoadedImages
from game.LoadedSounds import LoadedSounds
from game.tiles.Tile import Tile
from game.weathers.WeatherController import WeatherController

from game.entities.Player import Player
from game.entities.Boar import Boar
from game.entities.Bomb import Bomb
from game.entities.Deer import Deer
from game.entities.Rabbit import Rabbit
from game.entities.Goblin import Goblin

from game.objects.Grass import Grass
from game.objects.Rock import Rock
from game.objects.trees.LargeTree import LargeTree
from game.objects.trees.MediumTree import MediumTree
from game.objects.trees.SmallTree import SmallTree
from game.objects.trees.BurntTree import BurntTree
from game.objects.trees.Snag import Snag
from game.objects.trees.TreeSapling import TreeSapling
from game.objects.RabbitHole import RabbitHole
from game.objects.GoblinHideout import GoblinHideout

from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup

from game.items.Sword import Sword
from game.items.StoneAxe import StoneAxe
from game.items.StonePickaxe import StonePickaxe
from game.items.WoodenArmor import WoodenArmor
from game.items.LeatherArmor import LeatherArmor
from game.items.Accorn import Accorn
from game.items.Wood import Wood
from game.items.Pebble import Pebble
from game.items.SharpRock import SharpRock
from game.items.Leather import Leather
from game.items.DeerAntlers import DeerAntlers
from game.items.BoarFang import BoarFang
from game.items.GoblinFang import GoblinFang
from game.items.GrassFibers import GrassFibers
from game.items.SmallMeat import SmallMeat
from game.items.BigMeat import BigMeat
from game.items.LeatherArmor import LeatherArmor


class Game:
    def __init__(self, screen: Surface, config: Config, saveData: dict):
        self.config = config
        self.screen = screen
        self.generateMapLoadingScreen("Loading savefile")
        self.clock = Clock()

        self.loadedImages = LoadedImages()
        self.loadedSounds = LoadedSounds()

        self.visibleSprites = CameraSpriteGroup(config)
        self.obstacleSprites = ObstacleSprites(config)
        self.UiSprites = UiSpriteGroup(config, self.visibleSprites, self.loadedImages)

        self.tick = 0

        self.mapData = saveData['map']
        self.map = self.createMap(self.mapData)
        self.player: Player
        self.createSprites(saveData['sprites'])
        self.dayCycle = DayCycle(saveData['currentDay'], saveData['currentTimeMs'], 2 * 64 * 1000, self.clock, config, self.UiSprites, self.visibleSprites)

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

        sword = Sword(self.visibleSprites, Vector2(200, 200), self.loadedImages)
        self.player.inventory.addItem(sword, self.player.selectedItem)
        self.player.inventory.addItem(StoneAxe(self.visibleSprites, (0, 0), self.loadedImages), self.player.selectedItem)
        self.player.inventory.addItem(StonePickaxe(self.visibleSprites, (0, 0), self.loadedImages), self.player.selectedItem)
        self.player.inventory.addItem(WoodenArmor(self.visibleSprites, (0, 0), self.loadedImages), self.player.selectedItem)
        self.player.inventory.addItem(LeatherArmor(self.visibleSprites, (0, 0), self.loadedImages), self.player.selectedItem)

        self.inputManager = InputManager(self.player, self.UiSprites, self.visibleSprites, self.saveGame)


    def generateMapLoadingScreen(self, information: str) -> None:
        self.screen.fill((0, 0, 0))
        infoText = self.config.fontBig.render(information, True, FONT_MENU_COLOR)
        infoRect = infoText.get_rect(center=(0.5 * self.config.WINDOW_WIDTH, 0.5 * self.config.WINDOW_HEIGHT))
        self.screen.blit(infoText, infoRect)
        pygame.display.flip()

    def createMap(self, mapRaw: list[list[int]]):
        mapSize = len(mapRaw)
        map = populateMapWithData(mapRaw)

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

    def createSprites(self, sprites: dict) -> None:
        globalsData = globals()
        fixedArguments = {'visibleSprites': self.visibleSprites, 'obstacleSprites': self.obstacleSprites, 'UiSprites': self.UiSprites,
                           'loadedImages': self.loadedImages, 'loadedSounds': self.loadedSounds, 'config': self.config, 'clock': self.clock}
        for className, instancesDataList in sprites.items():
            if className == "Player":
                self.createPlayer(instancesDataList[0])
                continue
            classReference = globalsData[className]
            initArguments = inspect.getfullargspec(classReference.__init__).args[1:]
            # print('{:15s} {}'.format(className, initArguments))
            indexesOfArgumentsToReplace = []
            for argumentIndex in range(len(initArguments)):
                if initArguments[argumentIndex] in fixedArguments:
                    initArguments[argumentIndex] = fixedArguments[initArguments[argumentIndex]]
                else:
                    indexesOfArgumentsToReplace.append(argumentIndex)

            for instanceData in instancesDataList:
                instanceArguments = initArguments[:]
                for argumentIndex in indexesOfArgumentsToReplace:
                    # print(instanceData)
                    instanceArguments[argumentIndex] = instanceData[instanceArguments[argumentIndex]]
                classReference(*instanceArguments)

    def createPlayer(self, playerData: dict) -> None:
        self.player = Player(self.visibleSprites, self.obstacleSprites, self.UiSprites,
                        self.loadedImages, self.loadedSounds, self.config, self.clock,
                        playerData["midbottom"], playerData["currHealth"])

    def saveGame(self):
        savefileData = {'savefileName': self.config.savefileName,'currentDay': self.dayCycle.currentDay, 'currentTimeMs': self.dayCycle.currentTimeMs, "map": self.mapData}
        savefileData['sprites'] = self.visibleSprites.savefileGroups.createSavefileSpritesData()
        with open(f"savefiles/{self.config.savefileName}.json", "w") as file:
            dump(savefileData, file)

    def debug(self, text):
        img = self.config.fontTiny.render(text, True, (255, 255, 255))
        self.screen.blit(img, (10, 10))

    def handleTick(self):
        self.tick = self.tick + 1
        if self.tick == 1000:
            self.spawnBomb()
        if self.tick == 2000:
            self.tick = 0
            self.spawnBomb()
            self.player.heal(20)

    def spawnBomb(self):
        viablbePosition = False
        while not viablbePosition:
            viablbePosition = True
            randomFactor = random.choice([Vector2(1, 1), Vector2(-1, 1), Vector2(1, -1), Vector2(-1, -1)])
            offset = Vector2(random.randint(128, 512) * randomFactor.x, random.randint(128, 512) * randomFactor.y)
            position = Vector2(self.player.rect.centerx + offset.x, self.player.rect.centery + offset.y)
            rect = Rect(position, (20, 20))
            for sprite in self.obstacleSprites.getObstacles(position):
                if sprite.colliderRect.colliderect(rect):
                    viablbePosition = False
                    break
        Bomb(self.visibleSprites, self.obstacleSprites, self.loadedImages.bomb, self.loadedSounds.bomb, self.clock, position)

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
