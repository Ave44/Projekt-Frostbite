from pygame.math import Vector2
from pygame.sprite import Group

from game.dayCycle.DayCycle import DayCycle
from game.LoadedImages import LoadedImages
from game.items.Leather import Leather
from game.items.Wood import Wood
from game.items.domain.Hammer import Hammer
from game.lightning.Glowing import Glowing

from game.objects.domain.Object import Object
from game.entities.Player import Player
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class Tent(Object, Glowing):
    def __init__(self, visibleSprites: Group, obstacleSprites: ObstacleSprites, loadedImages: LoadedImages, midbottom: Vector2, dayCycle: DayCycle):
        self.loadedImages = loadedImages
        image = loadedImages.tent
        Object.__init__(self, visibleSprites, midbottom, 1, Hammer, image)
        self.dayCycle = dayCycle
        self.obstacleSprites = obstacleSprites
        tentSize = self.rect.size
        offset = Vector2(-100, -100) + Vector2(int(tentSize[0] * 0.5), int(tentSize[1] * 0.7))
        Glowing.__init__(self, loadedImages.mediumLight, self.rect, offset)

    def onLeftClickAction(self, player: Player) -> None:
        if self.dayCycle.isNight():
            self.dayCycle.skipNight()
            player.subtractHunger(20)

    def drop(self) -> None:
        Wood(self.visibleSprites, self.rect.midbottom, self.loadedImages)
        Leather(self.visibleSprites, self.rect.midbottom, self.loadedImages)
