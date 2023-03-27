from config import TILE_SIZE, BIOMES_ID
import random

def generateObjects(idMatrix: list[list[int]], probabilities: dict, progresNotiftFunc: callable) -> dict:
    biomesCoordinatesDict = getBiomesCoordinatesDict(idMatrix)
    
    trees = generateTrees(probabilities['tree'], biomesCoordinatesDict, progresNotiftFunc)
    rocks = generateRocks(probabilities['rock'], biomesCoordinatesDict, progresNotiftFunc)
    grasses = generateGrasses(probabilities['grass'], biomesCoordinatesDict, progresNotiftFunc)

    return {'trees': trees, 'rocks': rocks, 'grasses': grasses}

def getBiomesCoordinatesDict(idMatrix: list[list[int]]) -> dict:
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

def generateTrees(treeProbability: float, biomesCoordinatesDict: dict, progresNotiftFunc: callable) -> list[dict['midBottom': list[int, int], 'age': int, 'growthStage': int]]:
    trees = []
    if treeProbability > 0:
        progresNotiftFunc("Generating trees")
        spawnObjects(spawnTree, treeProbability, biomesCoordinatesDict['medow'], trees)
        spawnObjects(spawnTree, treeProbability * 4, biomesCoordinatesDict['forest'], trees)
        spawnObjects(spawnTree, treeProbability, biomesCoordinatesDict['swamp'], trees)
    return trees

def generateRocks(rockProbability: float, biomesCoordinatesDict: dict, progresNotiftFunc: callable) -> list[dict['midBottom': list[int, int]]]:
    rocks = []
    if rockProbability > 0:
        progresNotiftFunc("Generating rocks")
        spawnObjects(spawnRock, rockProbability * 0.8, biomesCoordinatesDict['medow'], rocks)
        spawnObjects(spawnRock, rockProbability * 8, biomesCoordinatesDict['rocky'], rocks)
        spawnObjects(spawnRock, rockProbability * 0.6, biomesCoordinatesDict['forest'], rocks)
    return rocks

def generateGrasses(grassProbability: float, biomesCoordinatesDict: dict, progresNotiftFunc: callable) -> list[dict['midBottom': list[int, int]]]:
    grasses = []
    if grassProbability > 0:
        progresNotiftFunc("Generating grasses")
        spawnObjects(spawnGrass, grassProbability, biomesCoordinatesDict['medow'], grasses)
        spawnObjects(spawnGrass, grassProbability * 0.1, biomesCoordinatesDict['forest'], grasses)
    return grasses

def spawnObjects(spawnObject: callable, probability: int, tiles: list[dict], objectsList: list[dict]) -> None:
    for tile in tiles:
        rand = random.random()
        while rand <= probability:
            position = [random.randint(0, TILE_SIZE) + tile['x'], random.randint(0, TILE_SIZE) + tile['y']]
            spawnObject(position, objectsList)
            rand += random.random()
    return objectsList

def spawnTree(position: list[int, int], treesList: list[dict]) -> None:
    age = random.randint(0, 10000)
    growthStage = random.randint(1, 3)
    treeData = {'midBottom': position, 'age': age, 'growthStage': growthStage}
    treesList.append(treeData)

def spawnRock(position: list[int, int], rocksList: list[dict]) -> None:
    rockData = {'midBottom': position}
    rocksList.append(rockData)

def spawnGrass(position: list[int, int], grassList: list[dict]) -> None:
    grassData = {'midBottom': position}
    grassList.append(grassData)
