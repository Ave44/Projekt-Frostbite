from perlin_noise import PerlinNoise
import random
import os
import pygame
from gameInitialization.PhasesOfMapGeneration import replaceGroundWithBeach, generateGroundAndWater
def loadImages():
    """
    Load images, so Tile class doesn't need to access filesystem million times, and map generation takes 10x faster
    Also makes it easier to define which tiles should be rendered as obstacles, when we have more obstacle sprites than 1
    Returns dict with ids of images and pygame image class attached to them( the one from pygrame.image.load() function)
    """
    dictOfImages={}
    idOfTile=0
    for biomeFolderName in os.listdir("./graphics/tiles"):
        dictOfImages[biomeFolderName]={"collidable":[],"walkable":[]}
        dictOfImages[biomeFolderName]["collidable"] = {}
        dictOfImages[biomeFolderName]["walkable"] = {}
        for collidableTileName in os.listdir("./graphics/tiles/" + biomeFolderName+"/collidable"):
            dictOfImages[biomeFolderName]["collidable"][idOfTile]=pygame.image.load("./graphics/tiles/" + biomeFolderName+"/collidable/"+collidableTileName)
            idOfTile+=1
        for walkableTileName in os.listdir("./graphics/tiles/" + biomeFolderName+"/walkable"):
            dictOfImages[biomeFolderName]["walkable"][idOfTile]=pygame.image.load("./graphics/tiles/" + biomeFolderName+"/walkable/"+walkableTileName)
            idOfTile += 1
    #print(dictOfImages)
    return dictOfImages

def loadImagesFileNames():
    """
    Load images, so Tile class doesn't need to access filesystem million times, and map generation takes 10x faster
    Also makes it easier to define which tiles should be rendered as obstacles, when we have more obstacle sprites than 1
    Returns dict with ids of images and name of image file attached to them
    """
    dictOfImages={}
    idOfTile=0
    for biomeFolderName in os.listdir("./graphics/tiles"):
        dictOfImages[biomeFolderName]={"collidable":[],"walkable":[]}
        dictOfImages[biomeFolderName]["collidable"] = {}
        dictOfImages[biomeFolderName]["walkable"] = {}
        for collidableTileName in os.listdir("./graphics/tiles/" + biomeFolderName+"/collidable"):
            dictOfImages[biomeFolderName]["collidable"][idOfTile]=collidableTileName
            idOfTile+=1
        for walkableTileName in os.listdir("./graphics/tiles/" + biomeFolderName+"/walkable"):
            dictOfImages[biomeFolderName]["walkable"][idOfTile]=walkableTileName
            idOfTile += 1
    print(dictOfImages)
    return dictOfImages



def generateMap(widthAndHeight=101):
    """Generate 2 dimensional map array for render function, to render.

        @param: widthAndHeight WidthAndHeight of 2 dimensional array. Can't be lower than 5.

        """

    dictOfImages=loadImages()
    dictOfImagesNames=loadImagesFileNames()

    mapAreaArray=generateGroundAndWater(widthAndHeight=widthAndHeight)
    mapAreaArray = replaceGroundWithBeach(1,mapAreaArray)

    # print the map
    #for line in mapAreaArray:
    #    print(line)
    return mapAreaArray
#generateMap(21)