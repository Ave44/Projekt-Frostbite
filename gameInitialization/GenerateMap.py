import os
import pygame
from perlin_noise import PerlinNoise
import random
from skimage.measure import label
import numpy as np
from math import sqrt
from constants import BIOMES_ID
from gameInitialization.GenerateSprites import GenerateSprites

def replaceIdWithNames(idMatrix: list[list[int]]) -> list[list[str]]:
    matrixSize = len(idMatrix)
    namesMatrix = [[BIOMES_ID[idMatrix[row][column]] for column in range(matrixSize)] for row in range(matrixSize)]

    for y in range(1, len(idMatrix) - 1):
        for x in range(1, len(idMatrix) - 1):
            if idMatrix[x][y] != 0:
                leftCoast = checkForBorder(idMatrix, namesMatrix, x, y,  0, -1, "L")
                rightCoast = checkForBorder(idMatrix, namesMatrix, x, y,  0,  1, "R")
                topCoast = checkForBorder(idMatrix, namesMatrix, x, y, -1,  0, "T")
                bottomCoast = checkForBorder(idMatrix, namesMatrix, x, y,  1,  0, "B")

                if not leftCoast and not topCoast:
                    checkForBorder(idMatrix, namesMatrix, x, y,  -1, -1, "1")
                if not rightCoast and not topCoast:
                    checkForBorder(idMatrix, namesMatrix, x, y,   1, -1, "2")
                if not rightCoast and not bottomCoast:
                    checkForBorder(idMatrix, namesMatrix, x, y,   1,  1, "3")
                if not leftCoast and not bottomCoast:
                    checkForBorder(idMatrix, namesMatrix, x, y,  -1,  1, "4")

    return namesMatrix

def checkForBorder(idMatrix: list[list[int]], namesMatrix: list[list[str]], x: int, y: int, xOffset: int, yOffset: int, borderTag: str) -> Bool:
    if idMatrix[x + xOffset][y + yOffset] == 0:
        namesMatrix[x][y] = namesMatrix[x][y] + borderTag
        return True
    return False

def loadTilesData() -> dict['image': pygame.image, 'walkable': bool]:
    tilesData = {}
    tileId = 0
    loadTilesByType(tilesData, tileId, "walkable", True)
    loadTilesByType(tilesData, tileId, "collidable", False)

    return tilesData

def loadTilesByType(tilesData: dict, tileId: int, subfolderName: str, isWalkable: bool) -> None:
    for biom in os.listdir(f"./graphics/tiles/{subfolderName}"):
        for imageFile in os.listdir(f"./graphics/tiles/{subfolderName}/{biom}"):
            name = imageFile[:-4]
            image = pygame.image.load(f"./graphics/tiles/{subfolderName}/{biom}/{imageFile}").convert()
            tilesData[name] = {"image": image, "walkable": isWalkable}
        tileId += 1

def populateNameMatrixWithData(namesMatrix: list[list[str]]) -> list[list[dict['image': pygame.image, 'walkable': bool]]]:
    tilesData = loadTilesData()
    mapSize = len(namesMatrix)
    dataMatrix = [[None for x in range(mapSize)] for y in range(mapSize)]

    for y in range(mapSize):
        for x in range(mapSize):
            dataMatrix[y][x] = tilesData[namesMatrix[y][x]]
    
    return dataMatrix

def generateMap(mapSize: int, objectsQuantity: float, progresNotifFunc: callable):
    progresNotifFunc("Generating map")
    idMatrix = generateIdMatrix(mapSize)

    namesMatrix = replaceIdWithNames(idMatrix)

    dataMatrix = populateNameMatrixWithData(namesMatrix)

    probabilities = {"Tree": 0.2, "Rock": 0.1, "Grass": 0.8, "RabbitHole": 0.01, "GoblinHideout": 0.01, "Deer": 0.02, "Boar": 0.03}
    probabilities = {key: value * objectsQuantity for key, value in probabilities.items()}
    sprites = GenerateSprites(idMatrix, probabilities, progresNotifFunc).sprites

    return idMatrix, dataMatrix, sprites

def populateMapWithData(idMatrix: list[list[int]]):
    namesMatrix = replaceIdWithNames(idMatrix)
    dataMatrix = populateNameMatrixWithData(namesMatrix)
    return dataMatrix

def generateIdMatrix(mapSize: int, seed=random.randint(1, 1000)):
    noise1 = PerlinNoise(octaves=5, seed=seed)
    noise2 = PerlinNoise(octaves=10, seed=seed)
    noise3 = PerlinNoise(octaves=20, seed=seed)

    noiseMatrix1 = []
    noiseMatrix2 = []
    
    for j in range(mapSize):
        noiseMatrix1row = []
        noiseMatrix2row = []
        for i in range(mapSize):
            noiseVal1 = noise1([i / mapSize, j / mapSize])
            noiseVal2 = noise2([i / mapSize, j / mapSize])
            noiseVal3 = noise3([i / mapSize, j / mapSize])
            noiseMatrix1row.append(noiseVal1 + noiseVal2 + noiseVal3)
            noiseMatrix2row.append(noiseVal1 + noiseVal2 * 0.5 + noiseVal3 * 0.25)
        noiseMatrix1.append(noiseMatrix1row)
        noiseMatrix2.append(noiseMatrix2row)

    noiseMatrixCombined = [[noiseMatrix2[y][x] + noiseMatrix1[y][x] for x in range(mapSize)] for y in range(mapSize)]

    noiseMatrixNormalized = normalize(noiseMatrixCombined)
    mask = getMask(noiseMatrixCombined)
    noiseMatrixMasked = [[noiseMatrixNormalized[y][x] * mask[y][x] for x in range(mapSize)] for y in range(mapSize)]
    
    idMatrix, binaryLandMatrix = setpFunc(noiseMatrixMasked)

    matrixAfterCleanup = cleanup(idMatrix, binaryLandMatrix, bridgeId=1)

    return matrixAfterCleanup

def normalize(matrix):
    maxValue = max(matrix[0])
    minValue = min(matrix[0])

    for row in matrix[1:]:
        maxValue = max(maxValue, max(row))
        minValue = min(minValue, min(row))
    dif = maxValue - minValue
    matrixNormalized = [[(x-minValue)/dif  for x in y] for y in matrix]

    return matrixNormalized

def setpFunc(matrix):
    step1 = 0.4
    step2 = 0.45
    step3 = 0.6
    matrixSize = len(matrix)
    newMatrix = [[0 for x in range(matrixSize)] for y in range(matrixSize)]
    land = [[0 for x in range(matrixSize)] for y in range(matrixSize)]
    for row in range(matrixSize):
        for column in range(matrixSize):
            curVal = matrix[row][column]
            newMatrix[row][column] = ((3 if curVal >= step3 else 2) if curVal >= step2 else 1) if curVal >= step1 else 0
            land[row][column] = 1 if curVal >= step1 else 0
    return newMatrix, land

def circleMask(matrix):
    matrixSize = len(matrix)
    center = matrixSize // 2
    mask = [[0 for x in range(matrixSize)] for y in range(matrixSize)]
    
    for y in range(matrixSize):
        for x in range(matrixSize):
            distance = ((x - center)**2 + (y - center)**2) / 2
            mask[y][x] = distance

    normalizedMask = normalize(mask)
    for y in range(matrixSize):
        for x in range(matrixSize):
            normalizedMask[y][x] = abs(normalizedMask[y][x] - 1)

    return normalizedMask

def rectangleMask(matrix):
    frameWidth = 30
    matrixSize = len(matrix)
    mask = [[0 for x in range(matrixSize)] for y in range(matrixSize)]
    
    for y in range(matrixSize):
        for x in range(matrixSize):
            distance = 0
            if x < frameWidth:
                distance = frameWidth - x
            if x > matrixSize - frameWidth:
                distance = frameWidth + x - matrixSize

            if y < frameWidth:
                distance = max(frameWidth - y, distance)
            if y > matrixSize - frameWidth:
                distance = max(frameWidth + y - matrixSize, distance)
            mask[y][x] = distance

    normalizedMask = normalize(mask)
    for y in range(matrixSize):
        for x in range(matrixSize):
            normalizedMask[y][x] = abs(normalizedMask[y][x] - 1)

    return normalizedMask

def getMask(matrix):
    matrixSize = len(matrix)
    circularMask = circleMask(matrix)
    rectangularMask = rectangleMask(matrix)
    combinedMask = [[circularMask[y][x] * rectangularMask[y][x] for x in range(matrixSize)] for y in range(matrixSize)]

    return combinedMask

def cleanup(matrix, binaryMatrix, bridgeId):
    afterRemoval, binaryMatrixAfterRemoval = removeSmallUnconnectedIslands(matrix, binaryMatrix)
    afterConnecting = connectIslands(afterRemoval, binaryMatrixAfterRemoval, bridgeId)

    return afterConnecting

def removeSmallUnconnectedIslands(matrix, binaryMatrix):
    matrixSize = len(matrix)
    matrixLabeled, islandsAmmount = label(np.array(binaryMatrix), return_num=True)
    newMatrix = [[matrix[y][x] for x in range(matrixSize)] for y in range(matrixSize)]
    newBinaryMatrix = [[binaryMatrix[y][x] for x in range(matrixSize)] for y in range(matrixSize)]

    islandSizes = [0 for islandIndex in range(islandsAmmount + 1)]

    for row in matrixLabeled:
        for val in row:
            islandSizes[val] += 1

    for row in range(matrixSize):
        for column in range(matrixSize):
            if islandSizes[matrixLabeled[row][column]] < 100:
                newMatrix[row][column] = 0
                newBinaryMatrix[row][column] = 0

    return newMatrix, newBinaryMatrix

def connectIslands(matrix, binaryMatrix, bridgeId):
    matrixSize = len(matrix)
    matrixLabeled, islandsAmmount = label(np.array(binaryMatrix), return_num=True)
    newMatrix = [[matrix[y][x] for x in range(matrixSize)] for y in range(matrixSize)]

    islandsOutline, islandsPoints = getIslandsOutline(matrixLabeled, islandsAmmount)

    distances = []
    distanceMatrix = [[0 for i in range(islandsAmmount)] for j in range(islandsAmmount)]
    pointsMatrix = [[0 for i in range(islandsAmmount)] for j in range(islandsAmmount)]
    for firstIndex in range(islandsAmmount - 1):
        label1 = firstIndex + 1
        for secondIndex in range(islandsAmmount - 1 - firstIndex):    
            label2 = secondIndex + firstIndex + 2
            data = findClosestPoints(islandsPoints[label1], islandsPoints[label2])
            distances.append({'label1': label1, 'label2': label2, 'data': data})
            distanceMatrix[label1 - 1][label2 - 1] = data['distance']
            distanceMatrix[label2 - 1][label1 - 1] = data['distance']
            pointsMatrix[label1 - 1][label2 - 1] = data
            pointsMatrix[label2 - 1][label1 - 1] = data

    islandsToConnect = minimalSpanningTree(distanceMatrix)

    for pair in islandsToConnect:
        l1, l2 = pair['label1'], pair['label2']
        bridge = pointsMatrix[l1][l2]
        point1 = bridge['point1']
        point2 = bridge['point2']
        createBridge(newMatrix, point1, point2, bridgeId)

    return newMatrix

def getIslandsOutline(matrixLabeled, islandsAmmount):
    matrixSize = len(matrixLabeled)
    islandsOutline = [[matrixLabeled[y][x] for x in range(matrixSize)] for y in range(matrixSize)]
    islandsPoints = [[] for island in range(islandsAmmount + 1)]
    for row in range(matrixSize):
        for column in range(matrixSize):
            if matrixLabeled[row - 1][column] != 0 and matrixLabeled[row + 1][column] != 0 and matrixLabeled[row][column - 1] != 0 and matrixLabeled[row][column + 1] != 0:
                islandsOutline[row][column] = 0
            else:
                islandsPoints[islandsOutline[row][column]].append({'x': column, 'y': row})
    return islandsOutline, islandsPoints

def findClosestPoints(pointsList1, pointsList2):
    minDistance = float('inf')
    list1Len = len(pointsList1)
    list2Len = len(pointsList2)
    point1 = None
    point2 = None
    for index1 in range(list1Len):
        for index2 in range(list2Len):
            p1 = pointsList1[index1]
            p2 = pointsList2[index2]
            distance = sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2)
            if minDistance > distance:
                minDistance = distance
                point1 = p1
                point2 = p2

    return {'distance': minDistance, 'point1': point1, 'point2': point2}

def minimalSpanningTree(matrix):
    matrixSize = len(matrix)
    visitedNodes = [False for node in range(matrixSize)]
    result = [[0 for column in range(matrixSize)] for row in range(matrixSize)]
    
    index = 0
    while(False in visitedNodes):
        minimum = float('inf')
        start = 0
        end = 0
        for p1 in range(matrixSize):
            if visitedNodes[p1]:
                for p2 in range(matrixSize):
                    if (not visitedNodes[p2] and matrix[p1][p2]>0):  
                        if matrix[p1][p2] < minimum:
                            minimum = matrix[p1][p2]
                            start, end = p1, p2
        visitedNodes[end] = True
        result[start][end] = minimum
        if minimum == float('inf'):
            result[start][end] = 0
        index += 1
        result[end][start] = result[start][end]

    edges = []
    for l1 in range(len(result)):
        for l2 in range(0+l1, len(result)):
            if result[l1][l2] != 0:
                edges.append({'label1': l1, 'label2': l2})
    return edges

def createBridge(matrix, point1, point2, bridgeId):
    xGrowth = point2['x'] - point1['x']
    yGrowth = point2['y'] - point1['y']
    horizontalStep = 1
    verticalStep = 1
    if xGrowth < 0:
        horizontalStep = -1
        xGrowth = xGrowth * -1
    if yGrowth < 0:
        verticalStep = -1
        yGrowth = yGrowth * -1
    directionRatio = xGrowth
    currPoint = point1
    rand1 = random.random()
    rand2 = random.random()
    while currPoint != point2:
        rand1 = min(max(rand1 + random.uniform(-0.5, 0.5), 0), 1)
        rand2 = min(max(rand2 + random.uniform(-0.5, 0.5), 0), 1)
        if directionRatio >= yGrowth:
            directionRatio -= yGrowth
            currPoint['x'] += horizontalStep
            createHorizontalStep(matrix, currPoint, bridgeId, rand1, rand2)
        else:
            directionRatio += xGrowth
            currPoint['y'] += verticalStep
            createVerticalStep(matrix, currPoint, bridgeId, rand1, rand2)

def createHorizontalStep(matrix, point, val, rand1=random.random(), rand2=random.random()):
    if rand1 > 0.5:
        matrix[point['y'] - 2][point['x']] = val
    matrix[point['y'] - 1][point['x']] = val
    matrix[point['y']][point['x']] = val
    matrix[point['y'] + 1][point['x']] = val
    if rand2 > 0.5:
        matrix[point['y'] + 2][point['x']] = val

def createVerticalStep(matrix, point, val, rand1=random.random(), rand2=random.random()):
    if rand1 > 0.5:
        matrix[point['y']][point['x'] - 2] = val
    matrix[point['y']][point['x'] - 1] = val
    matrix[point['y']][point['x']] = val
    matrix[point['y']][point['x'] + 1] = val
    if rand2 > 0.5:
        matrix[point['y']][point['x'] + 2] = val
