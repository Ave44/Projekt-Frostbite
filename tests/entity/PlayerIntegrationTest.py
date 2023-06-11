from unittest import TestCase
from unittest.mock import Mock

from pygame import Vector2, Surface
from pygame.sprite import Group
from pygame.time import Clock

from Config import Config
from game.LoadedImages import LoadedImages
from game.LoadedSounds import LoadedSounds
from game.entities.Player import Player
from game.items.LeatherArmor import LeatherArmor
from game.items.Sword import Sword
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup


class PlayerIntegrationTest(TestCase):
    def setUp(self) -> None:
        config = Mock(Config)
        config.WINDOW_HEIGHT = 0
        config.WINDOW_WIDTH = 0
        visibleSprites = Mock(CameraSpriteGroup)
        visibleSprites.entities = Group()
        visibleSprites.items = Group()
        visibleSprites.savefileGroups = Group()
        visibleSprites.savefileGroups.Player = Group()
        visibleSprites.savefileGroups.LeatherArmor = Group()
        visibleSprites.savefileGroups.Sword = Group()
        obstacleSprites = Group()
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
        loadedImages.leatherArmor = Surface((0, 0))
        loadedImages.sword = Surface((0, 0))
        uiSprites = UiSpriteGroup(config, visibleSprites, loadedImages)
        loadedSounds = Mock(LoadedSounds)
        loadedSounds.player = dict
        clock = Clock()
        self.playerPos = Vector2(0, 0)
        self.playerHealth = 100
        self.player = Player(visibleSprites, obstacleSprites, uiSprites, loadedImages, loadedSounds, config, clock,
                             self.playerPos, self.playerHealth)
        self.leatherArmor = LeatherArmor(visibleSprites, self.playerPos, loadedImages)
        self.weapon = Sword(visibleSprites, self.playerPos, loadedImages)

    def test_player_should_get_lower_damage_when_armor_is_equipped(self):
        self.player.bodySlot.item = self.leatherArmor

        self.player.getDamage(10)

        self.assertEqual(self.player.currHealth, self.playerHealth - 6)

    def test_player_should_deal_higher_damage_when_weapon_is_equipped(self):
        self.player.handSlot.item = self.weapon

        damageDealt = self.player.damage()

        self.assertEqual(damageDealt, 10)
