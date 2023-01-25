import os
import skimage
def rescaleGraphicsInFolder(relativeFolderParth,rescaleTimesThisNumber):
    for nameOfImageFile in os.listdir("./"+relativeFolderParth):
        filepath=relativeFolderParth+"/"+nameOfImageFile
        image = skimage.io.imread(filepath)
        image = skimage.transform.resize(image,(len(image)*rescaleTimesThisNumber,len(image[0])*rescaleTimesThisNumber),
                                         anti_aliasing=False,preserve_range=True,order=0).astype('uint8')
        skimage.io.imsave(filepath, skimage.img_as_ubyte(image))
        print(nameOfImageFile)
rescaleTimesThisNumber=2
rescaleGraphicsInFolder("items",rescaleTimesThisNumber)
rescaleGraphicsInFolder("player",rescaleTimesThisNumber)
rescaleGraphicsInFolder("tiles/collidable/sea",rescaleTimesThisNumber)
rescaleGraphicsInFolder("tiles/walkable/grassland",rescaleTimesThisNumber)
rescaleGraphicsInFolder("ui",rescaleTimesThisNumber)