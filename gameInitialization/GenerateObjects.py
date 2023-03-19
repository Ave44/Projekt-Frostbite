from config import TILE_SIZE, BIOMES_ID
import random

def GenerateObjects(idMatrix: list[list[int]], probabilities: dict, progresNotiftFunc: callable) -> dict:
    biomesCoordinatesDict = getBiomesCoordinatesDict(idMatrix)
    
    treeProbability = probabilities['tree']
    trees = []
    if treeProbability > 0:
        progresNotiftFunc("Generating trees")
        generateObjects(spawnTree, treeProbability, biomesCoordinatesDict['medow'], trees)
        generateObjects(spawnTree, treeProbability * 4., biomesCoordinatesDict['forest'], trees)
        generateObjects(spawnTree, treeProbability, biomesCoordinatesDict['swamp'], trees)

    rockProbability = probabilities['rock']
    rocks = []
    if rockProbability > 0:
        progresNotiftFunc("Generating rocks")
        generateObjects(spawnRock, rockProbability * 0.8, biomesCoordinatesDict['medow'], rocks)
        generateObjects(spawnRock, rockProbability * 8, biomesCoordinatesDict['rocky'], rocks)
        generateObjects(spawnRock, rockProbability * 0.6, biomesCoordinatesDict['forest'], rocks)

    grassProbability = probabilities['grass']
    grasses = []
    if grassProbability > 0:
        progresNotiftFunc("Generating grasses")
        generateObjects(spawnGrass, rockProbability, biomesCoordinatesDict['medow'], grasses)
        generateObjects(spawnGrass, rockProbability * 0.1, biomesCoordinatesDict['forest'], grasses)

    return {'trees': trees, 'rocks': rocks, 'grasses': grasses}

def getBiomesCoordinatesDict(idMatrix: list[list[int]]) -> dict:
    matrixSize = len(idMatrix)
    {0: 'sea', 1: 'beach', 2: 'medow', 3: 'forest', 4: 'rocky', 5: 'swamp'}
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

def generateObjects(spawnObject: callable, probability: int, tiles: list[dict], objectsList: list[dict]) -> None:
    # objectsList = []
    for tile in tiles:
        rand = random.random()
        while rand <= probability:
            position = [random.randint(0, TILE_SIZE) + tile['x'], random.randint(0, TILE_SIZE) + tile['y']]
            spawnObject(position, objectsList)
            rand += probability
    return objectsList

def spawnTree(position: list[int, int], treesList: list[dict]) -> None:
    treeSize = random.random()
    age = random.randint(0, 10000)
    treeData = {'midBottom': position, 'age': age}
    if treeSize < 0.3:
        treeData = {'midBottom': position, 'age': age, 'growthStage': 1}
        treesList.append(treeData)
    elif treeSize < 0.6:
        treeData = {'midBottom': position, 'age': age, 'growthStage': 2}
        treesList.append(treeData)
    else:
        treeData = {'midBottom': position, 'age': age, 'growthStage': 3}
        treesList.append(treeData)

def spawnRock(position: list[int, int], rocksList: list[dict]) -> None:
    rockData = {'midBottom': position}
    rocksList.append(rockData)

def spawnGrass(position: list[int, int], grassList: list[dict]) -> None:
    grassData = {'midBottom': position}
    grassList.append(grassData)
