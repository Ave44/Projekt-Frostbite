from PIL import Image
import numpy

from matplotlib import pyplot as plt


def makeArrayOftileSizextileSizeCoastImagesForTile(groundTilePath, seaTilePath, groundTileName, tileSize):
    '''After running function you can find new coast images in coastFiles folder'''

    def layMaskOnGroundFile(maskArray):
        for i in range(0, tileSize):
            for ii in range(0, tileSize):
                if maskArray[i][ii][0] == 0 and maskArray[i][ii][1] == 0 and maskArray[i][ii][2] == 0:
                    returnedTileArray[i][ii] = seaTileArray[i][ii]

    groundTileImg = Image.open(groundTilePath)
    #groundTileArray = numpy.array(groundTileImg)
    seaTileImg = Image.open(seaTilePath)
    seaTileArray = numpy.array(seaTileImg)

    # region BeachSidesRegion
    maskArray = numpy.array(Image.open("coastImageMakerMasks/mask1side.png"))
    mask2SideArray = numpy.array(Image.open("coastImageMakerMasks/mask2side.png"))
    maskCornerArray = numpy.array(Image.open("coastImageMakerMasks/maskcorner.png"))
    maskCorner3SideArray = numpy.array(Image.open("coastImageMakerMasks/maskcorner3side.png"))
    # 1 side beach
    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskArray)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "T.png")
    Image.fromarray(numpy.rot90(returnedTileArray)).save("coastFiles/" + groundTileName + "L.png")
    Image.fromarray(numpy.rot90(returnedTileArray, 2)).save("coastFiles/" + groundTileName + "B.png")
    Image.fromarray(numpy.rot90(returnedTileArray, 3)).save("coastFiles/" + groundTileName + "R.png")
    # corner side beach
    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskCornerArray)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "RT.png")
    Image.fromarray(numpy.rot90(returnedTileArray)).save("coastFiles/" + groundTileName + "LT.png")
    Image.fromarray(numpy.rot90(returnedTileArray, 2)).save("coastFiles/" + groundTileName + "LB.png")
    Image.fromarray(numpy.rot90(returnedTileArray, 3)).save("coastFiles/" + groundTileName + "RB.png")
    # 2 side beach
    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(mask2SideArray)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "LR.png")
    Image.fromarray(numpy.rot90(returnedTileArray)).save("coastFiles/" + groundTileName + "TB.png")
    # 3 side beach
    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskCorner3SideArray)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "LRT.png")
    Image.fromarray(numpy.rot90(returnedTileArray)).save("coastFiles/" + groundTileName + "LTB.png")
    Image.fromarray(numpy.rot90(returnedTileArray, 2)).save("coastFiles/" + groundTileName + "LRB.png")
    Image.fromarray(numpy.rot90(returnedTileArray, 3)).save("coastFiles/" + groundTileName + "RTB.png")

    # endregion

    # region InverseCornersRegion
    maskInverseCorner1 = numpy.array(Image.open("coastImageMakerMasks/maskInverseCorner1.png"))
    maskInverseCorner2 = numpy.array(Image.open("coastImageMakerMasks/maskInverseCorner2.png"))
    maskInverseCorner3 = numpy.array(Image.open("coastImageMakerMasks/maskInverseCorner3.png"))
    maskInverseCorner4 = numpy.array(Image.open("coastImageMakerMasks/maskInverseCorner4.png"))

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskInverseCorner1)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "1.png")

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskInverseCorner2)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "2.png")

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskInverseCorner3)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "3.png")

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskInverseCorner4)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "4.png")

    maskInverseCorner12 = numpy.array(Image.open("coastImageMakerMasks/maskInverseCorner12.png"))
    maskInverseCorner14 = numpy.array(Image.open("coastImageMakerMasks/maskInverseCorner14.png"))
    maskInverseCorner23 = numpy.array(Image.open("coastImageMakerMasks/maskInverseCorner23.png"))
    maskInverseCorner34 = numpy.array(Image.open("coastImageMakerMasks/maskInverseCorner34.png"))

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskInverseCorner12)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "12.png")

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskInverseCorner14)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "14.png")

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskInverseCorner23)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "23.png")

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskInverseCorner34)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "34.png")

    maskInverseCorner123 = numpy.array(Image.open("coastImageMakerMasks/maskInverseCorner123.png"))
    maskInverseCorner124 = numpy.array(Image.open("coastImageMakerMasks/maskInverseCorner124.png"))
    maskInverseCorner134 = numpy.array(Image.open("coastImageMakerMasks/maskInverseCorner134.png"))
    maskInverseCorner234 = numpy.array(Image.open("coastImageMakerMasks/maskInverseCorner234.png"))

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskInverseCorner123)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "123.png")

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskInverseCorner124)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "124.png")

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskInverseCorner134)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "134.png")

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskInverseCorner234)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "234.png")

    maskInverseCorner1234 = numpy.array(Image.open("coastImageMakerMasks/maskInverseCorner1234.png"))

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskInverseCorner1234)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "1234.png")
    # endregion

    # region BeachesWithInverseCornersRegion
    maskT3 = numpy.array(Image.open("coastImageMakerMasks/BeachesWithInverseCornersFolder/maskT3.png"))

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskT3)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "T3.png")

    maskT4 = numpy.array(Image.open("coastImageMakerMasks/BeachesWithInverseCornersFolder/maskT4.png"))

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskT4)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "T4.png")

    maskB1 = numpy.array(Image.open("coastImageMakerMasks/BeachesWithInverseCornersFolder/maskB1.png"))

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskB1)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "B1.png")

    maskB2 = numpy.array(Image.open("coastImageMakerMasks/BeachesWithInverseCornersFolder/maskB2.png"))

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskB2)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "B2.png")

    #========================================================================================

    maskB12 = numpy.array(Image.open("coastImageMakerMasks/BeachesWithInverseCornersFolder/maskB12.png"))

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskB12)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "B12.png")

    maskL23 = numpy.array(Image.open("coastImageMakerMasks/BeachesWithInverseCornersFolder/maskL23.png"))

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskL23)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "L23.png")

    maskT34 = numpy.array(Image.open("coastImageMakerMasks/BeachesWithInverseCornersFolder/maskT34.png"))

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskT34)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "T34.png")

    maskR14 = numpy.array(Image.open("coastImageMakerMasks/BeachesWithInverseCornersFolder/maskR14.png"))

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskR14)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "R14.png")

    # ========================================================================================

    maskLB2 = numpy.array(Image.open("coastImageMakerMasks/BeachesWithInverseCornersFolder/maskLB2.png"))

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskLB2)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "LB2.png")

    maskLT3 = numpy.array(Image.open("coastImageMakerMasks/BeachesWithInverseCornersFolder/maskLT3.png"))

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskLT3)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "LT3.png")

    maskRT4 = numpy.array(Image.open("coastImageMakerMasks/BeachesWithInverseCornersFolder/maskRT4.png"))

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskRT4)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "RT4.png")

    maskRB1 = numpy.array(Image.open("coastImageMakerMasks/BeachesWithInverseCornersFolder/maskRB1.png"))

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskRB1)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "RB1.png")

    # ========================================================================================

    maskL2 = numpy.array(Image.open("coastImageMakerMasks/BeachesWithInverseCornersFolder/maskL2.png"))

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskL2)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "L2.png")

    maskL3 = numpy.array(Image.open("coastImageMakerMasks/BeachesWithInverseCornersFolder/maskL3.png"))

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskL3)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "L3.png")

    maskR1 = numpy.array(Image.open("coastImageMakerMasks/BeachesWithInverseCornersFolder/maskR1.png"))

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskR1)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "R1.png")

    maskR4 = numpy.array(Image.open("coastImageMakerMasks/BeachesWithInverseCornersFolder/maskR4.png"))

    returnedTileArray = numpy.array(groundTileImg)
    layMaskOnGroundFile(maskR4)
    Image.fromarray(returnedTileArray).save("coastFiles/" + groundTileName + "R4.png")

    # end region

makeArrayOftileSizextileSizeCoastImagesForTile(
    "../../graphics/tiles/walkable/medow/medow.png",
    "../../graphics/tiles/collidable/sea/sea.png",
    "medow",
    128)
