import json
from pygame.time import Clock

from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup

from game.tiles.Tile import Tile

from game.LoadedImages import LoadedImages
from game.entities.Player import Player

from game.objects.trees.SmallTree import SmallTree
from game.objects.trees.MediumTree import MediumTree
from game.objects.trees.LargeTree import LargeTree
from game.objects.Rock import Rock
from game.objects.Grass import Grass

from Config import TILE_SIZE


class Store:
    def __init__(self, savefileData, savefileName) -> None:
        self.savefileName = savefileName

        self.clock = Clock()

        self.visibleSprites = CameraSpriteGroup()
        self.obstacleSprites = ObstacleSprites()
        self.uiSprites = UiSpriteGroup()

        self.map = savefileData.map
        self.loadMap()

        self.loadedImages = LoadedImages()

        self.loadObjects(savefileData.objects)

        self.player = self.createPlayer(savefileData)

    def saveToFilesave(self):
        data = {'map': self.map}

        data['player'] = {'position': self.player.rect.midBottom, 'currentHealth': self.player.currentHealth}

        data['trees'] = self.trees.map(lambda tree: {'midBottom': tree.rect.midbottom, 'age': tree.age, 'growthStage': tree.growthStage})
        data['rocks'] = self.rocks.map(lambda rock: {'midBottom': rock.rect.midbottom})
        data['grasses'] = self.grasses.map(lambda grass: {'midBottom': grass.rect.midbottom})

        fileSave = open(f'./savefiles/{self.savefileName}')
        json.dump(data, f'./savefiles/{self.savefileName}')
        fileSave.close()

    def loadMap(self):
        mapSize = len(self.map)
        tilesMap = [[None for x in range(mapSize)] for y in range(mapSize)]
        obstaclesMap = [[None for x in range(mapSize)] for y in range(mapSize)]
        for y in range(mapSize):
            for x in range(mapSize):
                xPos = x * TILE_SIZE
                yPos = y * TILE_SIZE
                tile = Tile((xPos, yPos), self.map[y][x]["image"])
                tilesMap[y][x] = tile
                if not self.map[y][x]["walkable"]:
                    obstaclesMap[y][x] = tile
        self.visibleSprites.map = tilesMap
        self.obstacleSprites.map = obstaclesMap

    def loadObjects(self, objects):
        self.loadTrees(objects['trees'])
        self.loadRocks(objects['rocks'])
        self.loadGrasses(objects['grasses'])

    def loadTrees(self, treesData):
        self.trees = []
        for treeData in treesData:
            if treeData['growthStage'] == 1:
                tree = SmallTree(self.visibleSprites, self.obstacleSprites, treeData['midBottom'], self.clock, treeData['age'])
            elif treeData['growthStage'] == 2:
                tree = MediumTree(self.visibleSprites, self.obstacleSprites, treeData['midBottom'], self.clock, treeData['age'])
            else:
                tree = LargeTree(self.visibleSprites, self.obstacleSprites, treeData['midBottom'], self.clock, treeData['age'])

            self.trees.append(tree)

    def loadRocks(self, rocksData):
        self.rocks = []
        for rockData in rocksData:
            rock = Rock(self.visibleSprites, self.obstacleSprites, rockData['midBottom'])
            self.rocks.append(rock)

    def loadGrasses(self, grassesData):
        self.grasses = []
        for grassData in grassesData:
            grass = Grass(self.visibleSprites, grassData['midBottom'])
            self.grasses.append(grass)

    def createPlayer(self, savefileData):
        return Player(self.visibleSprites,
                      self.obstacleSprites,
                      self.loadedImages.player,
                      self.clock,
                      savefileData.player['midBottom'],
                      savefileData.player['currHealth'])
