import random
import inspect
from os import remove
from json import dump
import pygame
from pygame import mixer, Surface, Rect, display, SRCALPHA
from pygame.math import Vector2
from pygame.time import Clock
from Config import Config
from constants import TILE_SIZE, HAPPY_THEME, SHADOW_COLOR
from game.SoundPlayer import SoundPlayer
from gameInitialization.GenerateMap import populateMapWithData
from game.dayCycle.DayCycle import DayCycle
from game.InputManager import InputManager
from game.LoadedImages import LoadedImages
from game.LoadedSounds import LoadedSounds
from game.tiles.Tile import Tile
from game.weathers.WeatherController import WeatherController
from game.ui.crafting.Crafting import Crafting

from game.entities.Player import Player
from game.entities.Boar import Boar
from game.entities.Bomb import Bomb
from game.entities.Deer import Deer
from game.entities.Rabbit import Rabbit
from game.entities.Goblin import Goblin
from game.entities.GoblinChampion import GoblinChampion

from game.objects.Grass import Grass
from game.objects.Rock import Rock
from game.objects.GoblinTorch import GoblinTorch
from game.objects.GoblinWatchTower import GoblinWatchTower
from game.objects.trees.LargeTree import LargeTree
from game.objects.trees.MediumTree import MediumTree
from game.objects.trees.SmallTree import SmallTree
from game.objects.trees.BurntTree import BurntTree
from game.objects.trees.Snag import Snag
from game.objects.trees.TreeSapling import TreeSapling
from game.objects.RabbitHole import RabbitHole
from game.objects.GoblinHideout import GoblinHideout
from game.objects.Tent import Tent

from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup
from game.items.Sword import Sword
from game.items.Mace import Mace
from game.items.StoneAxe import StoneAxe
from game.items.GoblinPickaxe import GoblinPickaxe
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
from menu.general.LoadingScreenGenerator import LoadingScreenGenerator


class Game:
    def __init__(self, config: Config, saveData: dict, returnToMainMenu: callable):
        self.config = config
        self.returnToMainMenu = returnToMainMenu
        self.screen = display.get_surface()
        LoadingScreenGenerator(config).generateLoadingScreen("Loading savefile")
        self.clock = Clock()

        self.loadedImages = LoadedImages()
        self.loadedSounds = LoadedSounds()

        self.visibleSprites = CameraSpriteGroup(config)
        self.obstacleSprites = ObstacleSprites(config)
        self.UiSprites = UiSpriteGroup(config, self.visibleSprites, self.loadedImages)
        self.soundPlayer = SoundPlayer()

        self.tick = 0

        self.mapData = saveData['map']
        self.map = self.createMap(self.mapData)
        self.player: Player
        self.dayCycle = DayCycle(saveData['currentDay'], saveData['currentTimeMs'], self.clock, config,
                                 self.UiSprites, self.visibleSprites)
        self.createSprites(saveData['sprites'])

        self.weatherController = WeatherController(self.loadedImages, self.clock, config,
                                                   Vector2(self.player.rect.center))
        self.visibleSprites.weatherController = self.weatherController

        if saveData['sprites']['Player'][0]['inventoryData'] == None:
            self.player.inventory.addItem(Sword(self.visibleSprites, self.player.rect.midbottom, self.loadedImages), self.player.selectedItem)
            self.player.inventory.addItem(StoneAxe(self.visibleSprites, self.player.rect.midbottom, self.loadedImages), self.player.selectedItem)
            self.player.inventory.addItem(StonePickaxe(self.visibleSprites, self.player.rect.midbottom, self.loadedImages), self.player.selectedItem)
            self.player.inventory.addItem(WoodenArmor(self.visibleSprites, self.player.rect.midbottom, self.loadedImages), self.player.selectedItem)
            self.player.inventory.addItem(LeatherArmor(self.visibleSprites, self.player.rect.midbottom, self.loadedImages), self.player.selectedItem)

        self.crafting = Crafting(config, self.visibleSprites, self.loadedImages)
        self.UiSprites.crafting = self.crafting

        self.inputManager = InputManager(self.player, self.UiSprites, self.visibleSprites, self.saveGame)
        self.towersAmount: int = len(saveData['sprites']['GoblinWatchTower'])

        self.gameRunning = True
        self.endMessage = None
        self.waitingForInput = False

    def destroyTower(self) -> None:
        self.towersAmount -= 1
        if self.towersAmount == 0:
            self.endGame("Victory!")

    def createMap(self, mapRaw: list[list[int]]) -> list[list]:
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
                          'loadedImages': self.loadedImages, 'loadedSounds': self.loadedSounds,
                          'config': self.config, 'clock': self.clock,
                          'soundPlayer': self.soundPlayer, 'destroyTower': self.destroyTower, 'dayCycle': self.dayCycle}
        playerInventoryData = None
        for className, instancesDataList in sprites.items():
            # print(className, len(instancesDataList))
            if className == "Player":
                self.createPlayer(instancesDataList[0])
                playerInventoryData = instancesDataList[0]["inventoryData"]
                continue
            classReference = globalsData[className]
            initArguments = inspect.getfullargspec(classReference.__init__).args[1:]
            # print('{:15s} {}\t{}'.format(className, len(instancesDataList), initArguments))
            indexesOfArgumentsToReplace = []
            for argumentIndex in range(len(initArguments)):
                if initArguments[argumentIndex] in fixedArguments:
                    initArguments[argumentIndex] = fixedArguments[initArguments[argumentIndex]]
                else:
                    indexesOfArgumentsToReplace.append(argumentIndex)

            for instanceData in instancesDataList:
                instanceArguments = initArguments[:]
                for argumentIndex in indexesOfArgumentsToReplace:
                    # print(className, instanceArguments)
                    instanceArguments[argumentIndex] = instanceData[instanceArguments[argumentIndex]]
                classReference(*instanceArguments)
        if playerInventoryData:
            self.player.populateEquipment(playerInventoryData)

    def createPlayer(self, playerData: dict) -> None:
        self.player = Player(self.visibleSprites, self.obstacleSprites, self.UiSprites,
                             self.loadedImages, self.loadedSounds, self.config, self.clock, self.endGame,
                             playerData["midbottom"], playerData["currHealth"], playerData['currHunger'])

    def saveGame(self):
        savefileData = {'savefileName': self.config.savefileName, 'currentDay': self.dayCycle.currentDay,
                        'currentTimeMs': self.dayCycle.currentTimeMs, "map": self.mapData,
                        'sprites': self.visibleSprites.savefileGroups.createSavefileSpritesData()}
        with open(f"savefiles/{self.config.savefileName}.json", "w") as file:
            dump(savefileData, file)

    def drawStatistics(self, text) -> None:
        img = self.config.fontTiny.render(text, True, (255, 255, 255))
        self.screen.blit(img, (10, 10))

    def handleTick(self) -> None:
        self.tick = self.tick + 1
        if self.tick == 1000:
            self.spawnBomb()
        if self.tick == 2000:
            self.tick = 0
            self.spawnBomb()
            self.player.heal(20)

    def spawnBomb(self) -> None:
        viablePosition = False
        while not viablePosition:
            viablePosition = True
            randomFactor = random.choice([Vector2(1, 1), Vector2(-1, 1), Vector2(1, -1), Vector2(-1, -1)])
            offset = Vector2(random.randint(128, 512) * randomFactor.x, random.randint(128, 512) * randomFactor.y)
            position = Vector2(self.player.rect.centerx + offset.x, self.player.rect.centery + offset.y)
            rect = Rect(position, (20, 20))
            for sprite in self.obstacleSprites.getObstacles(position):
                if sprite.colliderRect.colliderect(rect):
                    viablePosition = False
                    break
        Bomb(self.visibleSprites, self.obstacleSprites, self.loadedImages, self.loadedSounds, self.clock, position)

    def changeMusicTheme(self, theme) -> None:
        mixer.music.load(theme)
        mixer.music.play(-1)

    def endGame(self, endMessage: str) -> None:
        self.gameRunning = False
        self.endMessage = endMessage

    def displayEndMessage(self):
        grayScreen = Surface((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT), SRCALPHA)
        grayScreen.fill(SHADOW_COLOR)

        endMessage = self.config.fontHuge.render(self.endMessage, True, "White")
        endMessageRect = endMessage.get_rect(center=(0.5 * self.config.WINDOW_WIDTH, 0.5 * self.config.WINDOW_HEIGHT))

        escapeMessage = self.config.font.render("press any key to return to menu", True, "White")
        escapeMessageRect = escapeMessage.get_rect(center=(0.5 * self.config.WINDOW_WIDTH, 0.75 * self.config.WINDOW_HEIGHT))

        self.screen.blit(grayScreen, (0, 0))
        self.screen.blit(endMessage, endMessageRect)
        self.screen.blit(escapeMessage, escapeMessageRect)
        pygame.display.update()

        remove(f"./savefiles/{self.config.savefileName}.json")
        self.waitingForInput = True

    def play(self) -> None:
        self.changeMusicTheme(HAPPY_THEME)
        while self.gameRunning:
            self.inputManager.handleInput()
            self.dayCycle.update()
            self.visibleSprites.update()
            self.handleTick()
            playerCenter = Vector2(self.player.rect.center)
            self.weatherController.update(playerCenter)
            self.visibleSprites.customDraw(playerCenter)
            self.soundPlayer.currentCameraPos = playerCenter

            self.UiSprites.customDraw()

            gameStatistics = f"x:{self.player.rect.centerx}, y:{self.player.rect.centery}, {self.clock.get_fps()}"
            self.drawStatistics(gameStatistics)

            pygame.display.update()
            self.clock.tick()

        self.displayEndMessage()
        
        while self.waitingForInput:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.waitingForInput = False
                self.returnToMainMenu()
