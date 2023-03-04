import os
import pygame
from perlin_noise import PerlinNoise
import random
import matplotlib.pyplot as plt

biomesId = {0: 'sea', 1: 'grassland', 2: 'forest', 3: 'rocky'}

def generateIdMatrix(mapSize: int, seed=random.randint(1, 1000)):
    octaves = 10
    noise = PerlinNoise(octaves, seed)
    pic = [[noise([i / mapSize, j / mapSize]) for j in range(mapSize)] for i in range(mapSize)]

    idMatrix = [[0 for x in range(mapSize)] for y in range(mapSize)]

    r = (mapSize - 2) // 2 + 1
    for y in range(mapSize):
        for x in range(mapSize):
            if abs((x - (mapSize // 2)) ** 2 + (y - (mapSize // 2)) ** 2) < r ** 2 and pic[x][y] < 0.2:
                idMatrix[x][y] = 1
            else:
                idMatrix[x][y] = 0

    # TODO: temporal solution
    newIdMatrix = [[0 for x in range(mapSize + 20)] for y in range(mapSize + 20)]
    for y in range(mapSize):
        for x in range(mapSize):
            newIdMatrix[x + 10][y + 10] = idMatrix[x][y]
    return newIdMatrix

def replaceIdWithNames(idMatrix):
    namesMatrix = [[biomesId[idMatrix[row][column]] for column in range(len(idMatrix))] for row in range(len(idMatrix))]

    for y in range(1, len(idMatrix) - 1):
        for x in range(1, len(idMatrix) - 1):
            if idMatrix[x][y] != 0:
                checkForBorder(idMatrix, namesMatrix, x, y,  0, -1, "L")
                checkForBorder(idMatrix, namesMatrix, x, y,  0,  1, "R")
                checkForBorder(idMatrix, namesMatrix, x, y, -1,  0, "T")
                checkForBorder(idMatrix, namesMatrix, x, y,  1,  0, "B")

    return namesMatrix

def checkForBorder(idMatrix, namesMatrix, x: int, y: int, xOffset: int, yOffset: int, borderTag: str):
    if idMatrix[x + xOffset][y + yOffset] == 0:
        namesMatrix[x][y] = namesMatrix[x][y] + borderTag

# returns {name: {image: pygame.image, walkable: bool}} loading all images in advance makes the code faster
def loadTilesData():
    tilesData = {}
    tileId = 0
    loadTilesByType(tilesData, tileId, "walkable", True)
    loadTilesByType(tilesData, tileId, "collidable", False)

    return tilesData

def loadTilesByType(tilesData: dict, tileId: int, subfolderName: str, isWalkable: bool):
    for biom in os.listdir(f"./graphics/tiles/{subfolderName}"):
        for imageFile in os.listdir(f"./graphics/tiles/{subfolderName}/{biom}"):
            name = imageFile[:-4]
            image = pygame.image.load(f"./graphics/tiles/{subfolderName}/{biom}/{imageFile}")
            tilesData[name] = {"image": image, "walkable": isWalkable}
        tileId += 1

def populateNameMatrixWithData(namesMatrix):
    tilesData = loadTilesData()
    mapSize = len(namesMatrix)
    dataMatrix = [[None for x in range(mapSize)] for y in range(mapSize)]

    for y in range(mapSize):
        for x in range(mapSize):
            dataMatrix[y][x] = tilesData[namesMatrix[y][x]]
    
    return dataMatrix


def generateMap(mapSize: int):
    idMatrix = generateIdMatrix(mapSize)
    namesMatrix = replaceIdWithNames(idMatrix)
    dataMatrix = populateNameMatrixWithData(namesMatrix)

    return dataMatrix

def generateIdMatrix2(mapSize: int, seed=random.randint(1, 1000)):
    noise1 = PerlinNoise(octaves=5, seed=seed)
    noise2 = PerlinNoise(octaves=10, seed=seed)
    noise3 = PerlinNoise(octaves=20, seed=seed)
    pic1 = []
    pic2 = []
    pic3 = []
    pic4 = []
    pic5 = []
    pic6 = []
    
    for j in range(mapSize):
        row1 = []
        row2 = []
        row3 = []
        row4 = []
        row5 = []
        row6 = []
        for i in range(mapSize):
            noiseVal1 = noise1([i / mapSize, j / mapSize])
            noiseVal2 = noise2([i / mapSize, j / mapSize])
            noiseVal3 = noise3([i / mapSize, j / mapSize])
            row1.append(noiseVal1)
            row2.append(noiseVal2)
            row3.append(noiseVal1 + noiseVal2)
            row4.append(noiseVal1 + noiseVal2 * 0.5)
            row5.append(noiseVal1 + noiseVal2 + noiseVal3)
            row6.append(noiseVal1 + noiseVal2 * 0.5 + noiseVal3 * 0.25)
        pic1.append(row1)
        pic2.append(row2)
        pic3.append(row3)
        pic4.append(row4)
        pic5.append(row5)
        pic6.append(row6)

    idMatrix = [[0 for x in range(mapSize)] for y in range(mapSize)]
    pic7 = [[pic6[y][x] + pic5[y][x] for x in range(mapSize)] for y in range(mapSize)]

    pic1N = normalize(pic1)
    pic2N = normalize(pic2)
    pic3N = normalize(pic3)
    pic4N = normalize(pic4)
    pic5N = normalize(pic5)
    pic6N = normalize(pic6)
    pic7N = normalize(pic7)
    mask = getMask(pic7)
    pic8N = [[pic7N[y][x] * mask[y][x] for x in range(mapSize)] for y in range(mapSize)]
    
    plt.figure(figsize=(18,8))
    plt.suptitle("normalized noise", fontsize=16)

    plt.subplot(2,4,1)
    plt.imshow(pic1N, cmap='gray')
    plt.colorbar()
    plt.title("5")

    plt.subplot(2,4,5)
    plt.imshow(pic2N, cmap='gray')
    plt.colorbar()
    plt.title("10")

    plt.subplot(2,4,2)
    plt.imshow(pic3N, cmap='gray')
    plt.colorbar()
    plt.title("5 + 10")

    plt.subplot(2,4,6)
    plt.imshow(pic4N, cmap='gray')
    plt.colorbar()
    plt.title("5 + 10 * 0.5")

    plt.subplot(2,4,3)
    plt.imshow(pic5N, cmap='gray')
    plt.colorbar()
    plt.title("5 + 10 + 20")

    plt.subplot(2,4,7)
    plt.imshow(pic6N, cmap='gray')
    plt.colorbar()
    plt.title("5 + 10 * 0.5 + 20 * 0.25")
    
    plt.subplot(2,4,4)
    plt.imshow(pic7N, cmap='gray')
    plt.colorbar()
    plt.title("combined")

    plt.subplot(2,4,8)
    plt.imshow(pic8N, cmap='gray')
    plt.colorbar()
    plt.title("masked")

    pic1 = setpFunc(pic1N)
    pic2 = setpFunc(pic2N)
    pic3 = setpFunc(pic3N)
    pic4 = setpFunc(pic4N)
    pic5 = setpFunc(pic5N)
    pic6 = setpFunc(pic6N)
    pic7 = setpFunc(pic7N)
    pic8 = setpFunc(pic8N)
    plt.figure(figsize=(18,8))
    plt.suptitle("after step func", fontsize=16)

    plt.subplot(2,4,1)
    plt.imshow(pic1, cmap='gray')
    plt.colorbar()
    plt.title("5")

    plt.subplot(2,4,5)
    plt.imshow(pic2, cmap='gray')
    plt.colorbar()
    plt.title("10")

    plt.subplot(2,4,2)
    plt.imshow(pic3, cmap='gray')
    plt.colorbar()
    plt.title("5 + 10")

    plt.subplot(2,4,6)
    plt.imshow(pic4, cmap='gray')
    plt.colorbar()
    plt.title("5 + 10 * 0.5")

    plt.subplot(2,4,3)
    plt.imshow(pic5, cmap='gray')
    plt.colorbar()
    plt.title("5 + 10 + 20")

    plt.subplot(2,4,7)
    plt.imshow(pic6, cmap='gray')
    plt.colorbar()
    plt.title("5 + 10 * 0.5 + 20 * 0.25")
    
    plt.subplot(2,4,4)
    plt.imshow(pic7, cmap='gray')
    plt.colorbar()
    plt.title("combined")

    plt.subplot(2,4,8)
    plt.imshow(pic8, cmap='gray')
    plt.colorbar()
    plt.title("masked")
    plt.show()

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
    for row in range(matrixSize):
        for column in range(matrixSize):
            curVal = matrix[row][column]
            newMatrix[row][column] = ((1 if curVal >= step3 else 0.5) if curVal >= step2 else 0.25) if curVal >= step1 else 0
    return newMatrix



# map = generateIdMatrix2(256)

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

generateIdMatrix2(256)