from unittest import TestCase
from unittest.mock import Mock

import pygame
from pygame import Vector2, KEYDOWN, KEYUP, Surface, K_d, K_s
from pygame.event import Event
from pygame.locals import K_a, KMOD_NONE, K_w
from pygame.sprite import Group
from pygame.time import Clock

from Config import Config
from game.Game import Game
from game.InputManager import InputManager
from game.LoadedImages import LoadedImages
from game.LoadedSounds import LoadedSounds
from game.entities.Player import Player
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup


class InputManagerIntegrationTest(TestCase):
    def setUp(self) -> None:
        config = Mock(Config)
        config.WINDOW_HEIGHT = 0
        config.WINDOW_WIDTH = 0
        config.TILES_ON_SCREEN_HEIGHT = 0
        config.TILES_ON_SCREEN_WIDTH = 0
        visibleSprites = Mock(CameraSpriteGroup)
        visibleSprites.entities = Group()
        visibleSprites.savefileGroups = Group()
        visibleSprites.savefileGroups.Player = Group()
        obstacleSprites = Group()
        obstacleSprites.getObstacles = (lambda x: [])
        loadedImages = Mock(LoadedImages)
        loadedImages.player = {
            "idle": Surface((0, 0)),
            "movement": Surface((0, 0)),
            "attack": Surface((0, 0)),
            "damaged": Surface((0, 0)),

            "image_up": Surface((0, 0)),
            "image_down": Surface((0, 0)),
            "image_left": Surface((0, 0)),
            "image_right": Surface((0, 0)),

            "image_up_heal": Surface((0, 0)),
            "image_down_heal": Surface((0, 0)),
            "image_left_heal": Surface((0, 0)),
            "image_right_heal": Surface((0, 0)),

            "image_up_damage": Surface((0, 0)),
            "image_down_damage": Surface((0, 0)),
            "image_left_damage": Surface((0, 0)),
            "image_right_damage": Surface((0, 0)),
        }
        loadedImages.largeLight = Surface((0, 0))
        loadedImages.pointer = Surface((0, 0))
        loadedImages.slot = Surface((0, 0))
        loadedImages.slotHand = Surface((0, 0))
        loadedImages.slotBody = Surface((0, 0))
        uiSprites = UiSpriteGroup(config, visibleSprites, loadedImages)
        loadedSounds = Mock(LoadedSounds)
        loadedSounds.player = dict
        clock = Clock()
        saveGame = (lambda x: x)
        self.playerPos = Vector2(0, 0)
        self.player = Player(visibleSprites, obstacleSprites, uiSprites, loadedImages, loadedSounds, config, clock, self.playerPos)
        pygame.init()
        self.inputManager = InputManager(self.player, uiSprites, visibleSprites, saveGame)

    def test_player_should_move_forward_when_user_press_w(self):
        pygame.key.get_pressed = (lambda : {K_w: True, K_s: False, K_a: False, K_d: False})

        self.inputManager.handleInput()
        self.player.update()

        self.assertEqual(self.player.rect.midbottom, (self.playerPos.x, self.playerPos.y - 6))

    def test_player_should_move_left_when_user_press_a(self):
        pygame.key.get_pressed = (lambda : {K_w: False, K_s: False, K_a: True, K_d: False})

        self.inputManager.handleInput()
        self.player.update()

        self.assertEqual(self.player.rect.midbottom, (self.playerPos.x - 6, self.playerPos.y))

    def test_player_should_move_right_when_user_press_d(self):
        pygame.key.get_pressed = (lambda : {K_w: False, K_s: False, K_a: False, K_d: True})

        self.inputManager.handleInput()
        self.player.update()

        self.assertEqual(self.player.rect.midbottom, (self.playerPos.x + 6, self.playerPos.y))

    def test_player_should_move_behind_when_user_press_s(self):
        pygame.key.get_pressed = (lambda : {K_w: False, K_s: True, K_a: False, K_d: False})

        self.inputManager.handleInput()
        self.player.update()

        self.assertEqual(self.player.rect.midbottom, (self.playerPos.x, self.playerPos.y + 6))
