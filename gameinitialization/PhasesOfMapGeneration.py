from perlin_noise import PerlinNoise
import random
import os
import pygame
def generateGroundAndWater(widthAndHeight):
    noise = PerlinNoise(octaves=10, seed=random.randint(1, 1000))
    xpix, ypix = widthAndHeight, widthAndHeight
    pic = [[noise([i / xpix, j / ypix]) for j in range(xpix)] for i in range(ypix)]
    # print(pic)

    if (widthAndHeight < 5):
        return Exception("widthAndHeight parameter shouldn't be lower than 5 and it is.")
    a, b = widthAndHeight // 2, widthAndHeight // 2
    r = (widthAndHeight - 2) // 2 + 1

    mapAreaArray = [[0 for x in range(widthAndHeight)] for y in range(widthAndHeight)]  #

    for y in range(widthAndHeight):
        for x in range(widthAndHeight):
            if abs((x - a) ** 2 + (y - b) ** 2) < r ** 2 and pic[x][y] < 0.2:
                mapAreaArray[x][y] = 1
            else:
                mapAreaArray[x][y] = 0

    return mapAreaArray

def replaceGroundWithBeach(groundId,mapAreaArray):
    for y in range(1, len(mapAreaArray) - 1):#width
        for x in range(1,len(mapAreaArray[0])-1):#height
            #4 corenrsided beach tiles
            if (mapAreaArray[x][y] == 1 and mapAreaArray[x][y - 1] == 0 and mapAreaArray[x-1][y] == 0):
                mapAreaArray[x][y] = groundId+6#Top Left Corner Sided Beach
            elif (mapAreaArray[x][y] == 1 and mapAreaArray[x][y + 1] == 0 and mapAreaArray[x-1][y] == 0):
                mapAreaArray[x][y] = groundId+7#Top Right Corner Sided Beach
            elif (mapAreaArray[x][y] == 1 and mapAreaArray[x][y - 1] == 0 and mapAreaArray[x+1][y] == 0):
                mapAreaArray[x][y] = groundId+5#Bottom Left Corner Sided Beach
            elif (mapAreaArray[x][y] == 1 and mapAreaArray[x][y + 1] == 0 and mapAreaArray[x+1][y] == 0):
                mapAreaArray[x][y] = groundId+8#Bottom Right Corner Sided Beach
            #4 onesided beach tiles
            elif (mapAreaArray[x][y] == 1 and mapAreaArray[x][y - 1] == 0):
                mapAreaArray[x][y] = groundId+2#Left Sided Beach
            elif (mapAreaArray[x][y] == 1 and mapAreaArray[x][y + 1] == 0):
                mapAreaArray[x][y] = groundId+4#Right Sided Beach
            elif (mapAreaArray[x][y] == 1 and mapAreaArray[x-1][y] == 0):
                mapAreaArray[x][y] = groundId+3#Top Sided Beach
            elif (mapAreaArray[x][y] == 1 and mapAreaArray[x+1][y] == 0):
                mapAreaArray[x][y] = groundId+1#Bottom Sided Beach
            #2 twosided beach tiles
            if (mapAreaArray[x][y] >= groundId and mapAreaArray[x][y] < 15 and mapAreaArray[x-1][y] == 0 and mapAreaArray[x+1][y] == 0):
                mapAreaArray[x][y] = groundId+9# Top Bottom Sided Beach
            elif (mapAreaArray[x][y] >= groundId and mapAreaArray[x][y] < 15 and mapAreaArray[x][y - 1] == 0 and mapAreaArray[x][y + 1] == 0):
                mapAreaArray[x][y] = groundId+10# Right Left Sided Beach
            #4 threesided beach tiles
            if (mapAreaArray[x][y] >= groundId and mapAreaArray[x][y] < 15 and mapAreaArray[x-1][y] == 0 and mapAreaArray[x+1][y] == 0 and mapAreaArray[x][y + 1] == 0):
                mapAreaArray[x][y] = groundId+11# Top Bottom Right Sided Beach
            elif (mapAreaArray[x][y] >= groundId and mapAreaArray[x][y] < 15 and mapAreaArray[x-1][y] == 0 and mapAreaArray[x+1][y] == 0 and mapAreaArray[x][y - 1] == 0):
                mapAreaArray[x][y] = groundId+12# Top Bottom Left Sided Beach
            elif (mapAreaArray[x][y] >= groundId and mapAreaArray[x][y] < 15 and mapAreaArray[x][y - 1] == 0 and mapAreaArray[x][y + 1] == 0 and mapAreaArray[x+1][y] == 0):
                mapAreaArray[x][y] = groundId+13# Right Left Top Sided Beach
            elif (mapAreaArray[x][y] >= groundId and mapAreaArray[x][y] < 15 and mapAreaArray[x][y - 1] == 0 and mapAreaArray[x][y + 1] == 0 and mapAreaArray[x-1][y] == 0):
                mapAreaArray[x][y] = groundId+14# Right Left Bottom Sided Beach
            #1 all sided beach tile
            if(mapAreaArray[x][y] >= groundId and mapAreaArray[x][y] < 15
                    and mapAreaArray[x][y - 1] == 0 and mapAreaArray[x][y + 1] == 0
                    and mapAreaArray[x-1][y] == 0 and mapAreaArray[x+1][y] == 0):
                mapAreaArray[x][y] = groundId + 15

    return mapAreaArray