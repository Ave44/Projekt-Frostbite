from pygame import Vector2
from pygame.time import Clock

from game.entities.domain.AggressiveMob import AggressiveMob
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class Bomb(AggressiveMob):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: dict, midbottom: Vector2, clock: Clock, currHealth: int = None):
        entityData = {
            "speed": 3,
            "maxHealth": 60,
            "damage": 20,
            "sightRange": 400,
            "attackRange": 20
        }
        AggressiveMob.__init__(self, visibleSprites, obstacleSprites, loadedImages, entityData, clock, 200, 300, 500, 0, midbottom, currHealth)

    def afterAttackAction(self):
        self.die()

    def drop(self) -> None:
        pass
