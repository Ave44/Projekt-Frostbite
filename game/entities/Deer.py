from pygame import Vector2, Rect
from pygame.time import Clock

from game.entities.domain.PassiveMob import PassiveMob
from game.items.DeerAntlers import DeerAntlers
from game.items.Leather import Leather
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites
from game.LoadedSounds import LoadedSounds
from game.LoadedImages import LoadedImages


class Deer(PassiveMob):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: LoadedImages, loadedSounds: LoadedSounds, clock: Clock, midbottom: Vector2, currHealth: int = None):
        entityData = {
            "speed": 3,
            "maxHealth": 15,
            "actionRange": 20,
            "sightRange": 200,
            "moveEveryMs": 4000,
            "minMoveTimeMs": 1000,
            "maxMoveTimeMs": 2000
        }
        colliderRect = Rect((0, 0), (20, 20))
        PassiveMob.__init__(self, visibleSprites, obstacleSprites, loadedImages.deer, loadedSounds.deer, colliderRect, clock, entityData, midbottom, currHealth)
        self.loadedImages = loadedImages

    def drop(self) -> None:
        Leather(self.visibleSprites, self.rect.center, self.loadedImages)
        DeerAntlers(self.visibleSprites, self.rect.center, self.loadedImages)
