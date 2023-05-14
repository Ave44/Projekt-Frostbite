from pygame.math import Vector2
from pygame.sprite import Group

from game.DayCycle import DayCycle
from game.LoadedImages import LoadedImages
from game.items.domain.Hammer import Hammer

from game.objects.domain.Object import Object
from game.entities.Player import Player
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class Tent(Object):
    def __init__(self, visibleGroup: Group, obstacleSprites: ObstacleSprites, loadedImages: LoadedImages, midBottom: Vector2, dayCycle: DayCycle):
        self.loadedImages = loadedImages
        image = loadedImages.tent
        Object.__init__(self, visibleGroup, midBottom, 1, Hammer, image)
        self.dayCycle = dayCycle
        self.obstacleSprites = obstacleSprites

    def onLeftClickAction(self, player: Player) -> None:
        self.dayCycle.skipNight()
        player.subtractHunger(20)

    def drop(self) -> None:
        return

