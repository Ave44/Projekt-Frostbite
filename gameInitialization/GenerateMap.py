import os
import pygame
from perlin_noise import PerlinNoise
import random

biomesId = {0: 'sea', 1: 'grassland'}

def generateIdMatrix(mapSize: int, seed=random.randint(1, 1000)):
    octaves = 10
    noise = PerlinNoise(octaves, seed)
    pic = [[noise([i / mapSize, j / mapSize]) for j in range(mapSize)] for i in range(mapSize)]

    if (mapSize < 5):
        mapSize = 5

    idMatrix = [[0 for x in range(mapSize)] for y in range(mapSize)]

    r = (mapSize - 2) // 2 + 1
    for y in range(mapSize):
        for x in range(mapSize):
            if abs((x - (mapSize // 2)) ** 2 + (y - (mapSize // 2)) ** 2) < r ** 2 and pic[x][y] < 0.2:
                idMatrix[x][y] = 1
            else:
                idMatrix[x][y] = 0

    return idMatrix

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
    dataMap = [[None for x in range(mapSize)] for y in range(mapSize)]

    for y in range(mapSize):
        for x in range(mapSize):
            dataMap[y][x] = tilesData[namesMatrix[y][x]]
    
    return dataMap


def generateMap(mapSize: int):
    idMatrix = generateIdMatrix(mapSize)
    # for i in idMatrix:
    #     print(i)

    namesMatrix = replaceIdWithNames(idMatrix)
    # for i in namesMatrix:
    #     print(i)

    dataMatrix = populateNameMatrixWithData(namesMatrix)
    # for i in dataMatrix:
    #     print(i)

    return dataMatrix

# map = generateIdMatrix(64)
# a = replaceGroundWithBeach(1, map)
# for i in map:
#     for l in i:
#         if l == 1:
#             print("██", end="")
#         else:
#             print("  ", end="")
#         print(l, end="")
#     print("")

# generateMap(16)