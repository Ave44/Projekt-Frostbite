import os
import skimage
def rescaleGraphicsInFolder(relativeFolderParth,scale):
    for nameOfImageFile in os.listdir("./"+relativeFolderParth):
        filepath=relativeFolderParth+"/"+nameOfImageFile
        image = skimage.io.imread(filepath)
        image = skimage.transform.resize(image,(len(image)*scale,len(image[0])*scale),
                                         anti_aliasing=False,preserve_range=True,order=0).astype('uint8')
        skimage.io.imsave(filepath, skimage.img_as_ubyte(image))
        print(nameOfImageFile)
scale=2
rescaleGraphicsInFolder("items",scale)
rescaleGraphicsInFolder("player",scale)
rescaleGraphicsInFolder("tiles/collidable/sea",scale)
rescaleGraphicsInFolder("tiles/walkable/grassland",scale)
rescaleGraphicsInFolder("ui",scale)