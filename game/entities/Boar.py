from pygame import Vector2
from pygame.time import Clock

from game.entities.domain.AggressiveMob import AggressiveMob
from game.items.BigMeat import BigMeat
from game.items.BoarFang import BoarFang
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class Boar(AggressiveMob):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 clock: Clock, positionCenter: Vector2):
        entityData = {
            "speed": 2,
            "maxHealth": 30,
            "currentHealth": 30,
            "damage": 5,
            "sightRange": 100,
            "attackRange": 50,
            "position_center": positionCenter,
            "path_to_image_up": "./graphics/entities/boar/boar_up.png",
            "path_to_image_down": "./graphics/entities/boar/boar_down.png",
            "path_to_image_left": "./graphics/entities/boar/boar_left.png",
            "path_to_image_right": "./graphics/entities/boar/boar_right.png",

            "path_to_image_up_heal": "./graphics/entities/boar/boar_up_heal.png",
            "path_to_image_down_heal": "./graphics/entities/boar/boar_down_heal.png",
            "path_to_image_left_heal": "./graphics/entities/boar/boar_left_heal.png",
            "path_to_image_right_heal": "./graphics/entities/boar/boar_right_heal.png",

            "path_to_image_up_damage": "./graphics/entities/boar/boar_up_damage.png",
            "path_to_image_down_damage": "./graphics/entities/boar/boar_down_damage.png",
            "path_to_image_left_damage": "./graphics/entities/boar/boar_left_damage.png",
            "path_to_image_right_damage": "./graphics/entities/boar/boar_right_damage.png",
        }
        super().__init__(visibleSprites, obstacleSprites, entityData, clock, 700, 500, 1000, 2000)

    def afterAttackAction(self):
        pass

    def drop(self) -> None:
        BigMeat(self.visibleSprites, self.rect.center)
        BoarFang(self.visibleSprites, self.rect.center)
