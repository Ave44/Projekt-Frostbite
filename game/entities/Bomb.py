from pygame import Vector2
from pygame.time import Clock

from game.entities.domain.AggressiveMob import AggressiveMob
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class Bomb(AggressiveMob):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 positionCenter: Vector2, clock: Clock):
        entityData = {
            "speed": 3,
            "maxHealth": 60,
            "currentHealth": 60,
            "damage": 20,
            "sightRange": 400,
            "attackRange": 20,
            "position_center": positionCenter,
            "path_to_image_up": "./graphics/entities/enemy/enemy.png",
            "path_to_image_down": "./graphics/entities/enemy/enemy.png",
            "path_to_image_left": "./graphics/entities/enemy/enemy.png",
            "path_to_image_right": "./graphics/entities/enemy/enemy.png",

            "path_to_image_up_heal": "./graphics/entities/enemy/enemy.png",
            "path_to_image_down_heal": "./graphics/entities/enemy/enemy.png",
            "path_to_image_left_heal": "./graphics/entities/enemy/enemy.png",
            "path_to_image_right_heal": "./graphics/entities/enemy/enemy.png",

            "path_to_image_up_damage": "./graphics/entities/enemy/enemy.png",
            "path_to_image_down_damage": "./graphics/entities/enemy/enemy.png",
            "path_to_image_left_damage": "./graphics/entities/enemy/enemy.png",
            "path_to_image_right_damage": "./graphics/entities/enemy/enemy.png",
        }
        super().__init__(visibleSprites, obstacleSprites, entityData, clock)

    def afterAttackAction(self):
        self.die()
