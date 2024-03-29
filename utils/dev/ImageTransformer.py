import numpy
from imageio.v3 import imread, imwrite

from constants import ROOT_PATH


class ImageTransformerMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ImageTransformer(metaclass=ImageTransformerMeta):

    _GREEN_RGBA = [0, 255 * 0.3, 0, 0]
    _RED_RGBA = [255 * 0.3, 0, 0, 0]

    def createHealImage(self, relativeImageInPath: str, relativeImageOutPath: str = None):
        if not relativeImageOutPath:
            relativeImageOutPath = self._buildImageOutPath(relativeImageInPath, "_heal")

        im = imread(f"/{ROOT_PATH}/{relativeImageInPath}")
        healImage = self._transformImage(im, self._GREEN_RGBA)
        imwrite(f"/{ROOT_PATH}/{relativeImageOutPath}", healImage)

    def createDamageImage(self, relativeImageInPath: str, relativeImageOutPath: str = None):
        if not relativeImageOutPath:
            relativeImageOutPath = self._buildImageOutPath(relativeImageInPath, "_damage")

        im = imread(f"/{ROOT_PATH}/{relativeImageInPath}")
        damageImage = self._transformImage(im, self._RED_RGBA)
        imwrite(f"/{ROOT_PATH}/{relativeImageOutPath}", damageImage)

    @staticmethod
    def _buildImageOutPath(relativeImageInPath: str, typeOfImage: str):
        splitInPath = relativeImageInPath.split(".")
        imageOutPath = splitInPath[0] + typeOfImage + "." + splitInPath[1]
        return imageOutPath

    @staticmethod
    def _transformImage(image: numpy.ndarray, colorRGBA: list[int, int, int, int]) -> numpy.ndarray:
        imageCopy = numpy.array(image)
        imageCopy[imageCopy.sum() != 0] = numpy.add(imageCopy, colorRGBA)
        return imageCopy
