import unittest

import pygame

from Config import Config
from game.entities.domain.Entity import Entity
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class EntityTest(unittest.TestCase):
    entityData = {
        "position_center": [0, 0],
        "path_to_image_up": "./graphics/icon.png",
        "path_to_image_down": "./graphics/icon.png",
        "path_to_image_left": "./graphics/icon.png",
        "path_to_image_right": "./graphics/icon.png"
    }

    def test_entity_movement_diagonal_U_R(self):
        config = Config()
        entity = Entity(CameraSpriteGroup(config), pygame.sprite.Group(), self.entityData)
        entity.speed = 10
        entity.direction.x = 1
        entity.direction.y = 1
        entity.move()
        self.assertEqual(entity.rect.topleft, [7, 7], "Movement direction vector should be normalized")

    def test_entity_movement_diagonal_U_L(self):
        config = Config()
        entity = Entity(CameraSpriteGroup(config), pygame.sprite.Group(), self.entityData)
        entity.speed = 10
        entity.direction.x = -1
        entity.direction.y = 1
        entity.move()
        self.assertEqual(entity.rect.topleft, [-7, 7], "Movement direction vector should be normalized")

    def test_entity_movement_diagonal_D_R(self):
        config = Config()
        entity = Entity(CameraSpriteGroup(config), pygame.sprite.Group(), self.entityData)
        entity.speed = 10
        entity.direction.x = 1
        entity.direction.y = -1
        entity.move()
        self.assertEqual(entity.rect.topleft, [7, -7], "Movement direction vector should be normalized")

    def test_entity_movement_diagonal_D_L(self):
        config = Config()
        entity = Entity(CameraSpriteGroup(config), pygame.sprite.Group(), self.entityData)
        entity.speed = 10
        entity.direction.x = -1
        entity.direction.y = -1
        entity.move()
        self.assertEqual(entity.rect.topleft, [-7, -7], "Movement direction vector should be normalized")


if __name__ == '__main__':
    unittest.main()