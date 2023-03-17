import random

from pygame import Vector2
from pygame.time import Clock

from game.entities.Entity import Entity


class Rabbit(Entity):
    def __init__(self, spriteGroup, obstacleSprites, clock: Clock, positionCenter: Vector2):
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
        super().__init__(spriteGroup, obstacleSprites, entityData, clock)
        self.jumpingTime = 0
        self.jumpTime = 0
        self.timeBetweenJumps = 0

    def jump(self):
        self.timeBetweenJumps = 0
        self.jumpingTime = 0
        self.jumpTime = random.randint(500, 1000)
        self.direction = Vector2(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))

    def move(self):
        if self.direction.x != 0 and self.direction.y != 0:
            self.direction = self.direction.normalize()

        self.rect.x += round(self.direction.x * self.speed, 3)
        self.checkHorizontalCollision()

        self.rect.y += round(self.direction.y * self.speed, 3)
        self.checkVerticalCollision()

        self.adjustImageToDirection()

    def localUpdate(self):
        dt = self.clock.get_time()
        if self.jumpingTime < self.jumpTime:
            self.jumpingTime += dt
            self.move()
            return
        self.timeBetweenJumps += dt
        if self.timeBetweenJumps >= 2000:
            self.jump()
