from pygame import Vector2
from pygame.time import Clock

from game.entities.domain.PassiveMob import PassiveMob
from game.entities.domain.State import State
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites

class Rabbit(PassiveMob):

    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 clock: Clock, positionCenter: Vector2, homePositionCenter: Vector2 = None):

        entityData = {
            "speed": 2,
            "maxHealth": 5,
            "currentHealth": 5,
            "position_center": positionCenter,
            "path_to_image_up": "./graphics/entities/rabbit/rabbit_up.png",
            "path_to_image_down": "./graphics/entities/rabbit/rabbit_down.png",
            "path_to_image_left": "./graphics/entities/rabbit/rabbit_left.png",
            "path_to_image_right": "./graphics/entities/rabbit/rabbit_right.png",

            "path_to_image_up_damage": "./graphics/entities/rabbit/rabbit_up_damage.png",
            "path_to_image_down_damage": "./graphics/entities/rabbit/rabbit_down_damage.png",
            "path_to_image_left_damage": "./graphics/entities/rabbit/rabbit_left_damage.png",
            "path_to_image_right_damage": "./graphics/entities/rabbit/rabbit_right_damage.png",

            "path_to_image_up_heal": "./graphics/entities/rabbit/rabbit_up_heal.png",
            "path_to_image_down_heal": "./graphics/entities/rabbit/rabbit_down_heal.png",
            "path_to_image_left_heal": "./graphics/entities/rabbit/rabbit_left_heal.png",
            "path_to_image_right_heal": "./graphics/entities/rabbit/rabbit_right_heal.png"
        }
        super().__init__(visibleSprites, obstacleSprites, clock, entityData, 200, 2000, 500, 1500)
        self.homePosition = positionCenter
        self.isRunningHome = False
        self.isInHome = False
        self.isHomeless = False
        if not homePositionCenter:
            self.isHomeless = True

    def drop(self) -> None:
        pass

    def runHome(self):
        self.setDestination(self.homePosition, None)
        self.isRunningHome = True

    def hide(self):
        self.isRunningHome = False
        self.isInHome = True
        self.remove(*self.groups())

    def goOut(self):
        self.add(self.visibleSprites)
        self.isInHome = False

    def getDamage(self, amount: int) -> None:
        self.runHome()
        super().getDamage(amount)

    def localUpdate(self):
        if self.isHomeless:
            super().localUpdate()
        elif self.rect.midbottom == self.homePosition and self.isRunningHome:
            self.hide()
        elif self.destinationPosition:
            self.move()
        else:
            super().localUpdate()
