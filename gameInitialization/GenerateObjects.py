from constants import BIOMES_ID, TILE_SIZE
import random

class GenerateObjects:
    def __init__(self, idMatrix: list[list[int]], probabilities: dict, progresNotiftFunc: callable):
        self.biomesCoordinatesDict = self.getBiomesCoordinatesDict(idMatrix)
        self.probabilities = probabilities
        self.progresNotiftFunc = progresNotiftFunc

        self.objects = {}

        self.generateTrees()
        self.generateRocks()
        self.generateGrasses()

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

    def generateTrees(self) -> None:
        treeProbability = self.probabilities['tree']
        self.objects['trees'] = []
        if treeProbability > 0:
            self.progresNotiftFunc("Generating trees")
            self.spawnObjects(self.spawnTree, treeProbability, self.biomesCoordinatesDict['medow'])
            self.spawnObjects(self.spawnTree, treeProbability * 4, self.biomesCoordinatesDict['forest'])
            self.spawnObjects(self.spawnTree, treeProbability, self.biomesCoordinatesDict['swamp'])

    def generateRocks(self) -> None:
        rockProbability = self.probabilities['rock']
        self.objects['rocks'] = []
        if rockProbability > 0:
            self.progresNotiftFunc("Generating rocks")
            self.spawnObjects(self.spawnRock, rockProbability * 0.8, self.biomesCoordinatesDict['medow'])
            self.spawnObjects(self.spawnRock, rockProbability * 8, self.biomesCoordinatesDict['rocky'])
            self.spawnObjects(self.spawnRock, rockProbability * 0.6, self.biomesCoordinatesDict['forest'])

    def generateGrasses(self) -> None:
        grassProbability = self.probabilities['grass']
        self.objects['grasses'] = []
        if grassProbability > 0:
            self.progresNotiftFunc("Generating grasses")
            self.spawnObjects(self.spawnGrass, grassProbability, self.biomesCoordinatesDict['medow'])
            self.spawnObjects(self.spawnGrass, grassProbability * 0.1, self.biomesCoordinatesDict['forest'])
    
    def spawnObjects(self, spawnObject: callable, probability: int, tiles: list[dict]) -> None:
        for tile in tiles:
            rand = random.random()
            while rand <= probability:
                position = [random.randint(0, TILE_SIZE) + tile['x'], random.randint(0, TILE_SIZE) + tile['y']]
                spawnObject(position)
                rand += random.random()
        
    def spawnTree(self, position: list[int, int]) -> None:
        age = random.randint(0, 10000)
        growthStage = random.randint(1, 3)
        treeData = {'midBottom': position, 'age': age, 'growthStage': growthStage}
        self.objects['trees'].append(treeData)

    def spawnRock(self, position: list[int, int]) -> None:
        rockData = {'midBottom': position}
        self.objects['rocks'].append(rockData)

    def spawnGrass(self, position: list[int, int]) -> None:
        grassData = {'midBottom': position}
        self.objects['grasses'].append(grassData)
