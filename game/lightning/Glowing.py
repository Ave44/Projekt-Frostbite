from pygame import image as pyimage

from config import ROOT_PATH
from game.lightning.LightSize import LightSize


class Glowing:
    def __init__(self, size: LightSize):
        self.light = pyimage.load(f"{ROOT_PATH}/graphics/lights/light_{size.value}.png").convert_alpha()
