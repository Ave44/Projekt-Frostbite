from pygame import Vector2
from pygame.time import Clock

from game.entities.domain.AggressiveMob import AggressiveMob
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class Boar(AggressiveMob):
    def __init__(self, visibleSprites: CameraSpriteGroup, positionCenter: Vector2,
                 obstacleSprites: ObstacleSprites, clock: Clock):
        entityData = {
            "speed": 2,
            "maxHealth": 30,
            "currentHealth": 30,
            "damage": 5,
            "sightRange": 100,
            "attackRange": 50,
            "position_center": positionCenter,
            "path_to_image_up": "./graphics/entities/boar/boar.png",
            "path_to_image_down": "./graphics/entities/boar/boar.png",
            "path_to_image_left": "./graphics/entities/boar/boar.png",
            "path_to_image_right": "./graphics/entities/boar/boar.png",

            "path_to_image_up_heal": "./graphics/entities/boar/boar.png",
            "path_to_image_down_heal": "./graphics/entities/boar/boar.png",
            "path_to_image_left_heal": "./graphics/entities/boar/boar.png",
            "path_to_image_right_heal": "./graphics/entities/boar/boar.png",

            "path_to_image_up_damage": "./graphics/entities/boar/boar.png",
            "path_to_image_down_damage": "./graphics/entities/boar/boar.png",
            "path_to_image_left_damage": "./graphics/entities/boar/boar.png",
            "path_to_image_right_damage": "./graphics/entities/boar/boar.png",
        }
        super().__init__(visibleSprites, obstacleSprites, entityData, clock)

    def afterAttackAction(self):
        pass
