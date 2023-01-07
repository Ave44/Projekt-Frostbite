import os
import pygame
from perlin_noise import PerlinNoise
import random

biomesId = {0: 'sea', 1: 'grassland'}

def generateGroundAndWater(mapSize, seed=random.randint(1, 1000)):
    octaves = 10
    noise = PerlinNoise(octaves, seed)
    pic = [[noise([i / mapSize, j / mapSize]) for j in range(mapSize)] for i in range(mapSize)]

    if (mapSize < 5):
        mapSize = 5

    mapAreaArray = [[0 for x in range(mapSize)] for y in range(mapSize)]

    r = (mapSize - 2) // 2 + 1
    for y in range(mapSize):
        for x in range(mapSize):
            if abs((x - (mapSize // 2)) ** 2 + (y - (mapSize // 2)) ** 2) < r ** 2 and pic[x][y] < 0.2:
                mapAreaArray[x][y] = 1
            else:
                mapAreaArray[x][y] = 0

    return mapAreaArray

def replaceGroundWithBeach(mapAreaArray):
    tilesMatrix = [[biomesId[mapAreaArray[row][column]] for column in range(len(mapAreaArray))] for row in range(len(mapAreaArray))]

    for y in range(1, len(mapAreaArray) - 1):
        for x in range(1, len(mapAreaArray) - 1):
            if mapAreaArray[x][y] != 0:
                if mapAreaArray[x][y - 1] == 0:
                    tilesMatrix[x][y] = tilesMatrix[x][y] + "L"
                if mapAreaArray[x][y + 1] == 0:
                    tilesMatrix[x][y] = tilesMatrix[x][y] + "R"
                if mapAreaArray[x - 1][y] == 0:
                    tilesMatrix[x][y] = tilesMatrix[x][y] + "T"
                if mapAreaArray[x + 1][y] == 0:
                    tilesMatrix[x][y] = tilesMatrix[x][y] + "B"

    return tilesMatrix

# returns {name: {image: pygame.image, walkable: bool}} loading all images in advance makes the code faster
def loadTilesData():
    tilesData = {}
    tileId = 0
    for biom in os.listdir("./graphics/tiles/walkable"):
        for imageFile in os.listdir(f"./graphics/tiles/walkable/{biom}"):
            name = imageFile[:-4]
            image = pygame.image.load(f"./graphics/tiles/walkable/{biom}/{imageFile}")
            tilesData[name] = {"image": image, "walkable": True}
        tileId += 1
            
    for biom in os.listdir("./graphics/tiles/collidable"):
        for imageFile in os.listdir(f"./graphics/tiles/collidable/{biom}"):
            name = imageFile[:-4]
            image = pygame.image.load(f"./graphics/tiles/collidable/{biom}/{imageFile}")
            tilesData[name] = {"image": image, "walkable": False}
        tileId += 1

    return tilesData

def a(namesMap):
    tilesData = loadTilesData()
    mapSize = len(namesMap)
    dataMap = [[None for x in range(mapSize)] for y in range(mapSize)]

    for y in range(mapSize):
        for x in range(mapSize):
            dataMap[y][x] = tilesData[namesMap[y][x]]
    
    return dataMap


def generateMap(mapSize):
    idMap = generateGroundAndWater(mapSize)
    # for i in idMap:
    #     print(i)

    namesMap = replaceGroundWithBeach(idMap)
    # for i in namesMap:
    #     print(i)

    dataMap = a(namesMap)
    # for i in dataMap:
    #     print(i)

    return dataMap

# map = generateGroundAndWater(64)
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