from pygame import Vector2
from pygame.time import Clock
from game.LoadedImages import LoadedImages
from game.entities.domain.AnimatedEntity import AnimatedEntity

from game.entities.domain.AggressiveMob import AggressiveMob
from game.items.BigMeat import BigMeat
from game.items.GoblinFang import GoblinFang
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class Goblin(AggressiveMob, AnimatedEntity):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: LoadedImages, clock: Clock, midbottom: Vector2, currHealth: int = None):
        entityData = {
            "speed": 3,
            "maxHealth": 50,
            "damage": 10,
            "sightRange": 150,
            "actionRange": 50,
            "moveEveryMs": 700,
            "minMoveTimeMs": 500,
            "maxMoveTimeMs": 1000,
            "attackCooldownMs": 2000
        }
        AggressiveMob.__init__(self, visibleSprites, obstacleSprites, loadedImages.goblin, entityData, clock, midbottom, currHealth)
        self.loadedImages = loadedImages

    def drop(self) -> None:
        BigMeat(self.visibleSprites, self.rect.center, self.loadedImages)
        GoblinFang(self.visibleSprites, self.rect.center, self.loadedImages)
