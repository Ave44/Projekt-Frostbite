from constants import BIOMES_ID, TILE_SIZE
import random

class GenerateSprites:
    def __init__(self, idMatrix: list[list[int]], probabilities: dict, progresNotiftFunc: callable):
        self.biomesCoordinatesDict = self.getBiomesCoordinatesDict(idMatrix)
        self.probabilities = probabilities
        self.progresNotiftFunc = progresNotiftFunc

        self.sprites = {}

        self.createPlayer()
        self.generateTrees()
        self.generateRocks()
        self.generateGrasses()
        self.generateRabbitHoles()
        self.generateGoblinHideouts()
        self.generateDeers()
        self.generateBoars()

    def getBiomesCoordinatesDict(self, idMatrix: list[list[int]]) -> dict:
        matrixSize = len(idMatrix)

        biomesCoordinatesDict = {}
        for _, value in BIOMES_ID.items():
            biomesCoordinatesDict[value] = []

        for y in range(matrixSize):
            yCoordinate = y * TILE_SIZE
            for x in range(matrixSize):
                xCoordinate = x * TILE_SIZE
                coordinates = {'x': xCoordinate, 'y': yCoordinate}
                biome = BIOMES_ID[idMatrix[y][x]]
                biomesCoordinatesDict[biome].append(coordinates)
        
        return biomesCoordinatesDict

    def createPlayer(self) -> None:
        midbottom = (self.biomesCoordinatesDict['medow'][0]['x'] + 50, self.biomesCoordinatesDict['medow'][0]['y'] + 50)
        self.sprites['Player'] = [{'midbottom': midbottom, 'currHealth': None, 'currHunger': None, 'inventoryData': None}]
    

    def generateTrees(self) -> None:
        treeProbability = self.probabilities['Tree']
        self.sprites['SmallTree'] = []
        self.sprites['MediumTree'] = []
        self.sprites['LargeTree'] = []
        if treeProbability > 0:
            self.progresNotiftFunc("Generating trees")
            self.spawn(self.spawnTree, treeProbability, self.biomesCoordinatesDict['medow'])
            self.spawn(self.spawnTree, treeProbability * 4, self.biomesCoordinatesDict['forest'])
            self.spawn(self.spawnTree, treeProbability, self.biomesCoordinatesDict['swamp'])

    def generateRocks(self) -> None:
        rockProbability = self.probabilities['Rock']
        self.sprites['Rock'] = []
        if rockProbability > 0:
            self.progresNotiftFunc("Generating rocks")
            self.spawn(self.spawnRock, rockProbability * 0.8, self.biomesCoordinatesDict['medow'])
            self.spawn(self.spawnRock, rockProbability * 8, self.biomesCoordinatesDict['rocky'])
            self.spawn(self.spawnRock, rockProbability * 0.6, self.biomesCoordinatesDict['forest'])

    def generateGrasses(self) -> None:
        grassProbability = self.probabilities['Grass']
        self.sprites['Grass'] = []
        if grassProbability > 0:
            self.progresNotiftFunc("Generating grasses")
            self.spawn(self.spawnGrass, grassProbability, self.biomesCoordinatesDict['medow'])
            self.spawn(self.spawnGrass, grassProbability * 0.1, self.biomesCoordinatesDict['forest'])

    def generateRabbitHoles(self):
        rabbitHolesProbability = self.probabilities['RabbitHole']
        self.sprites['RabbitHole'] = []
        if rabbitHolesProbability > 0:
            self.progresNotiftFunc("Generating rabbit holes")
            self.spawn(self.spawnRabbitHole, rabbitHolesProbability, self.biomesCoordinatesDict['medow'])
            self.spawn(self.spawnRabbitHole, rabbitHolesProbability * 0.5, self.biomesCoordinatesDict['beach'])

    def generateGoblinHideouts(self):
        goblinHideoutProbability = self.probabilities['GoblinHideout']
        self.sprites['GoblinHideout'] = []
        if goblinHideoutProbability > 0:
            self.progresNotiftFunc("Generating goblin hideouts")
            self.spawn(self.spawnGoblinHideout, goblinHideoutProbability, self.biomesCoordinatesDict['forest'])
            self.spawn(self.spawnGoblinHideout, goblinHideoutProbability * 0.2, self.biomesCoordinatesDict['medow'])

    def generateDeers(self):
        deerProbability = self.probabilities['Deer']
        self.sprites['Deer'] = []
        if deerProbability > 0:
            self.progresNotiftFunc("Generating deers")
            self.spawn(self.spawnDeer, deerProbability, self.biomesCoordinatesDict['forest'])
            self.spawn(self.spawnDeer, deerProbability * 0.2, self.biomesCoordinatesDict['medow'])

    def generateBoars(self):
        boarProbability = self.probabilities['Boar']
        self.sprites['Boar'] = []
        if boarProbability > 0:
            self.progresNotiftFunc("Generating boars")
            self.spawn(self.spawnBoar, boarProbability, self.biomesCoordinatesDict['forest'])
            self.spawn(self.spawnBoar, boarProbability * 0.2, self.biomesCoordinatesDict['medow'])

    def spawnWatchTowers(self):
        towersToSpawn = 4
        currentlySpawned = 0
        self.progresNotiftFunc("Generating goblin watch towers")
        tiles = self.biomesCoordinatesDict['medow']
        for tile in tiles:
            if currentlySpawned < towersToSpawn:
                position = [random.randint(0, TILE_SIZE) + tile['x'], random.randint(0, TILE_SIZE) + tile['y']]
                goblinWatchTowerData = {'midbottom': position, "currentDurability": None}
                self.sprites['GoblinWatchTower'].append(goblinWatchTowerData)

    def spawn(self, spawnObject: callable, probability: int, tiles: list[dict]) -> None:
        for tile in tiles:
            rand = random.random()
            while rand <= probability:
                position = [random.randint(0, TILE_SIZE) + tile['x'], random.randint(0, TILE_SIZE) + tile['y']]
                spawnObject(position)
                rand += random.random()
        
    def spawnTree(self, position: list[int, int]) -> None:
        ageMs = random.randint(0, 10000)
        growthStage = random.randint(0, 2)
        growthStageNames = ['SmallTree', 'MediumTree', 'LargeTree']
        treeData = {'midbottom': position, 'ageMs': ageMs, "currentDurability": None}

        objectName = growthStageNames[growthStage]
        self.sprites[objectName].append(treeData)

    def spawnRock(self, position: list[int, int]) -> None:
        rockData = {'midbottom': position, "currentDurability": None}
        self.sprites['Rock'].append(rockData)

    def spawnGrass(self, position: list[int, int]) -> None:
        grassData = {'midbottom': position, "currentDurability": None, "currGrowthTime": None}
        self.sprites['Grass'].append(grassData)

    def spawnRabbitHole(self, position: list[int, int]) -> None:
        rabbitHoleData = {'midbottom': position, "currentDurability": None, "daysFromRabbitsChange": None, "rabbitsDataList": None}
        self.sprites['RabbitHole'].append(rabbitHoleData)

    def spawnGoblinHideout(self, position: list[int, int]) -> None:
        goblinHideoutData = {'midbottom': position, "currentDurability": None, "daysFromGoblinsChange": None, "goblinsDataList": None}
        self.sprites['GoblinHideout'].append(goblinHideoutData)

    def spawnDeer(self, position: list[int, int]) -> None:
        deerData = {'midbottom': position, 'currHealth': None}
        self.sprites['Deer'].append(deerData)

    def spawnBoar(self, position: list[int, int]) -> None:
        boarData = {'midbottom': position, 'currHealth': None}
        self.sprites['Boar'].append(boarData)
