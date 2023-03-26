from pygame import Vector2
from pygame.time import Clock

from game.entities.domain.PassiveMob import PassiveMob
from game.entities.domain.State import State
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class Deer(PassiveMob):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 clock: Clock, positionCenter: Vector2):
        entityData = {
            "speed": 3,
            "maxHealth": 15,
            "currentHealth": 15,
            "position_center": positionCenter,
            "path_to_image_up": "./graphics/entities/deer/deer_up.png",
            "path_to_image_down": "./graphics/entities/deer/deer_down.png",
            "path_to_image_left": "./graphics/entities/deer/deer_left.png",
            "path_to_image_right": "./graphics/entities/deer/deer_right.png",

            "path_to_image_up_damage": "./graphics/entities/deer/deer_up_damage.png",
            "path_to_image_down_damage": "./graphics/entities/deer/deer_down_damage.png",
            "path_to_image_left_damage": "./graphics/entities/deer/deer_left_damage.png",
            "path_to_image_right_damage": "./graphics/entities/deer/deer_right_damage.png",

            "path_to_image_up_heal": "./graphics/entities/deer/deer_up_heal.png",
            "path_to_image_down_heal": "./graphics/entities/deer/deer_down_heal.png",
            "path_to_image_left_heal": "./graphics/entities/deer/deer_left_heal.png",
            "path_to_image_right_heal": "./graphics/entities/deer/deer_right_heal.png"
        }
        super().__init__(visibleSprites, obstacleSprites, clock, entityData, 200, 4000, 1000, 2000)

    def drop(self) -> None:
        pass
