from PIL import Image
import numpy

from matplotlib import pyplot as plt


def makeArrayOf128x128CoastImagesForTile(groundTilePath, seaTilePath):
    groundTileImg = Image.open(groundTilePath)
    groundTileArray = numpy.array(groundTileImg)
    maskArray = numpy.array(Image.open("mask.png"))
    mask2SideArray = numpy.array(Image.open("mask2side.png"))
    maskCornerArray = numpy.array(Image.open("maskcorner.png"))
    maskCorner3SideArray = numpy.array(Image.open("maskcorner3side.png"))
    print(maskArray)
    returnedTileArray = groundTileArray
    returnedTilesArrays = []
    seaTilelImg = Image.open(seaTilePath)
    seaTileArray = numpy.array(seaTilelImg)

    # 1 side beach
    for i in range(0, 128):
        for ii in range(0, 128):
            if maskArray[i][ii][0] == 0 and maskArray[i][ii][1] == 0 and maskArray[i][ii][2] == 0:
                returnedTileArray[i][ii] = seaTileArray[i][ii]
    plt.imshow(returnedTileArray, interpolation='nearest')
    plt.show()
    # 2 side beach
    for i in range(0, 128):
        for ii in range(0, 128):
            if mask2SideArray[i][ii][0] == 0 and mask2SideArray[i][ii][1] == 0 and mask2SideArray[i][ii][2] == 0:
                returnedTileArray[i][ii] = seaTileArray[i][ii]
    plt.imshow(returnedTileArray, interpolation='nearest')
    plt.show()
    # 3 side beach




makeArrayOf128x128CoastImagesForTile(
    "../../graphics/tiles/walkable/beach/beach.png",
    "../../graphics/tiles/collidable/sea/sea.png")
