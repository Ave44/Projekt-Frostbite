from pygame import Vector2, Rect
from pygame.time import Clock
from game.LoadedImages import LoadedImages
from game.LoadedSounds import LoadedSounds

from game.entities.domain.AggressiveMob import AggressiveMob
from game.items.BigMeat import BigMeat
from game.items.BoarFang import BoarFang
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class Boar(AggressiveMob):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: LoadedImages, loadedSounds: LoadedSounds, clock: Clock, midbottom: Vector2, currHealth: int = None):
        entityData = {
            "speed": 2,
            "maxHealth": 30,
            "damage": 5,
            "sightRange": 100,
            "actionRange": 50,
            "moveEveryMs": 700,
            "minMoveTimeMs": 500,
            "maxMoveTimeMs": 1000,
            "attackCooldownMs": 2000
        }
        colliderRect = Rect((0, 0), (20, 20))
        AggressiveMob.__init__(self, visibleSprites, obstacleSprites, loadedImages.boar, loadedSounds.boar, colliderRect, entityData, clock, midbottom, currHealth)
        self.loadedImages = loadedImages

    def drop(self) -> None:
        BigMeat(self.visibleSprites, self.rect.center, self.loadedImages)
        BoarFang(self.visibleSprites, self.rect.center, self.loadedImages)
