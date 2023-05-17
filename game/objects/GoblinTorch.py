from pygame import Vector2
from game.LoadedImages import LoadedImages
from game.items.Wood import Wood
from game.items.domain.Axe import Axe

from game.lightning.Glowing import Glowing
from game.objects.domain.Object import Object
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class GoblinTorch(Object, Glowing):
    def __init__(self, visibleGroup: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: LoadedImages, midBottom: Vector2):
        image = loadedImages.goblinTorch
        Object.__init__(self, visibleGroup, midBottom, 50, Axe, image)
        self.loadedImages = loadedImages
        self.obstacleSprites = obstacleSprites
        torchSize = self.rect.size
        offset = Vector2(-100, -100) + Vector2(torchSize[0] // 2, torchSize[1] // 2)
        Glowing.__init__(self, loadedImages.mediumLight, self.rect, offset)


    def interact(self) -> None:
        print("interacted with goblin torch")

    def drop(self) -> None:
        Wood(self.visibleGroup, self.rect.center, self.loadedImages)

