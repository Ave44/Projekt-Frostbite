import random

from pygame import Vector2
from pygame.time import Clock

from game.entities.Entity import Entity


class Rabit(Entity):
    def __init__(self, spriteGroup, obstacleSprites, clock: Clock, positionCenter: Vector2):
        entityData = {
            'speed': 0,
            'maxHealth': 5,
            'currentHealth': 5,
            'position_center': positionCenter,
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
        super().__init__(spriteGroup, obstacleSprites, entityData, clock)
        self.isJumping = False
        self.jumpHeight = 100
        self.jumpSpeed = 5
        self.jumpFrames = 0
        self.timeBetweenJumps = 0

    def jump(self, direction: Vector2):
        self.isJumping = True
        self.jumpFrames = 10
        self.direction = direction

    def move(self):
        if self.direction.x != 0 and self.direction.y != 0:
            self.direction = self.direction.normalize()

        if self.jumpFrames >= -10:
            neg = 1
            if self.jumpFrames < 0:
                neg = -1
            self.rect.x += round(self.direction.x * self.jumpSpeed)
            self.checkHorizontalCollision()
            self.rect.y -= round((self.jumpFrames ** 2) * 0.5 * neg * self.direction.y)
            self.checkVerticalCollision()
        else:
            self.isJumping = False
            self.direction((1, 1))

        self.adjustImageToDirection()
        self.adjustDirection()

    def localUpdate(self):
        if self.isJumping:
            self.move()
            return
        if self.timeBetweenJumps >= 2000:
            direction = Vector2(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))
            self.jump(direction)
