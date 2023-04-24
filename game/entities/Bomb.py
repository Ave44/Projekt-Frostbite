from pygame import Vector2
from pygame.time import Clock

from game.entities.domain.AggressiveMob import AggressiveMob
from game.entities.domain.Entity import Entity
from game.objects.domain.Object import Object
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites
from game.LoadedSounds import LoadedSounds
from game.LoadedImages import LoadedImages


class Bomb(AggressiveMob):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: LoadedImages, loadedSounds: LoadedSounds, midbottom: Vector2, clock: Clock, currHealth: int = None):
        entityData = {
            "speed": 3,
            "maxHealth": 60,
            "damage": 20,
            "sightRange": 400,
            "actionRange": 20,
            "moveEveryMs": 4000,
            "minMoveTimeMs": 1000,
            "maxMoveTimeMs": 2000,
            "attackCooldownMs": 0
        }
        AggressiveMob.__init__(self, visibleSprites, obstacleSprites, loadedImages, loadedSounds, entityData, clock, midbottom, currHealth)

    def attack(self, target: Entity | Object):
        AggressiveMob.attack(self, target)
        self.die()

    def drop(self) -> None:
        pass
