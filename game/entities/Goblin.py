from pygame import Vector2
from pygame.time import Clock

from game.entities.domain.AggressiveMob import AggressiveMob
from game.items.BigMeat import BigMeat
from game.items.GoblinFang import GoblinFang
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites


class Goblin(AggressiveMob):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 clock: Clock, positionCenter: Vector2, home = None):
        entityData = {
            "speed": 2,
            "maxHealth": 30,
            "currentHealth": 30,
            "damage": 5,
            "sightRange": 100,
            "attackRange": 50,
            "position_center": positionCenter,
            "path_to_image_up": "./graphics/entities/goblin/goblin_up.png",
            "path_to_image_down": "./graphics/entities/goblin/goblin_down.png",
            "path_to_image_left": "./graphics/entities/goblin/goblin_left.png",
            "path_to_image_right": "./graphics/entities/goblin/goblin_right.png",

            "path_to_image_up_heal": "./graphics/entities/goblin/goblin_up_heal.png",
            "path_to_image_down_heal": "./graphics/entities/goblin/goblin_down_heal.png",
            "path_to_image_left_heal": "./graphics/entities/goblin/goblin_left_heal.png",
            "path_to_image_right_heal": "./graphics/entities/goblin/goblin_right_heal.png",

            "path_to_image_up_damage": "./graphics/entities/goblin/goblin_up_damage.png",
            "path_to_image_down_damage": "./graphics/entities/goblin/goblin_down_damage.png",
            "path_to_image_left_damage": "./graphics/entities/goblin/goblin_left_damage.png",
            "path_to_image_right_damage": "./graphics/entities/goblin/goblin_right_damage.png",
        }
        super().__init__(visibleSprites, obstacleSprites, entityData, clock, 700, 500, 1000, 2000)

    def afterAttackAction(self):
        pass

    def drop(self) -> None:
        BigMeat(self.visibleSprites, self.rect.center)
        GoblinFang(self.visibleSprites, self.rect.center)
