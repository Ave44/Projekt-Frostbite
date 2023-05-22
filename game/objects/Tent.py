from pygame.math import Vector2
from pygame.sprite import Group

from game.DayCycle import DayCycle
from game.LoadedImages import LoadedImages
from game.items.Leather import Leather
from game.items.Wood import Wood
from game.items.domain.Hammer import Hammer
from game.lightning.Glowing import Glowing

from game.objects.domain.Object import Object
from game.entities.Player import Player
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class Tent(Object, Glowing):
    def __init__(self, visibleGroup: Group, obstacleSprites: ObstacleSprites, loadedImages: LoadedImages, midBottom: Vector2, dayCycle: DayCycle):
        self.loadedImages = loadedImages
        image = loadedImages.tent
        Object.__init__(self, visibleGroup, midBottom, 1, Hammer, image)
        self.dayCycle = dayCycle
        self.obstacleSprites = obstacleSprites
        tentSize = self.rect.size
        offset = Vector2(-100, -100) + Vector2(tentSize[0] // 2, tentSize[1] // 2)
        Glowing.__init__(self, loadedImages.mediumLight, self.rect, offset)

    def onLeftClickAction(self, player: Player) -> None:
        if self.dayCycle.isNight():
            self.dayCycle.skipNight()
            player.subtractHunger(20)

    def drop(self) -> None:
        Wood(self.visibleSprites, self.rect.center, self.loadedImages)
        Leather(self.visibleSprites, self.rect.center, self.loadedImages)
