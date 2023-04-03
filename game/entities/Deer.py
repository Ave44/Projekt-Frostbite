from pygame import Vector2
from pygame.time import Clock
from game.LoadedImages import LoadedImages

from game.entities.domain.PassiveMob import PassiveMob
from game.items.DeerAntlers import DeerAntlers
from game.items.Leather import Leather
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class Deer(PassiveMob):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: LoadedImages, clock: Clock, midbottom: Vector2, currHealth: int = None):
        entityData = {
            "speed": 3,
            "maxHealth": 15
        }
        super().__init__(visibleSprites, obstacleSprites, loadedImages.deer, clock, entityData, 200, 4000, 1000, 2000, midbottom, currHealth)
        self.loadedImages = loadedImages

    def drop(self) -> None:
        Leather(self.visibleSprites, self.rect.center, self.loadedImages)
        DeerAntlers(self.visibleSprites, self.rect.center, self.loadedImages)
