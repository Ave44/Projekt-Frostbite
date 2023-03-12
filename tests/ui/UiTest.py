import unittest

import mock
from pygame import Vector2

from config import *
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.ui.inventory.Inventory import Inventory


class UiTest(unittest.TestCase):

    def setUp(self) -> None:
        visibleSprite = CameraSpriteGroup()
        self.playerPos = (3, 56)
        self.inventory = Inventory(visibleSprite, 2, 2, Vector2())

    @mock.patch("pygame.mouse")
    @mock.patch("game.ui.inventory.Inventory")
    def test_handleMouseLeftClick_should_call_inventory_handleMouseLeftClick_once(self, _, mockInventory):
        self.inventory = mockInventory
        self.inventory.handleMouseLeftClick()

        mockInventory.handleMouseLeftClick.assert_called_once()

    @mock.patch("pygame.mouse")
    @mock.patch("game.ui.inventory.Inventory")
    def test_handleMouseRightClick_should_call_inventory_handleMouseRightClick_once(self, _, mockInventory):
        self.inventory = mockInventory
        self.inventory.handleMouseRightClick()

        mockInventory.handleMouseRightClick.assert_called_once()

    @mock.patch("game.ui.inventory.Inventory")
    def test_toggleInventory_should_call_toggle_on_inventory_once(self, mockInventory):
        self.inventory = mockInventory
        self.inventory.toggle()

        mockInventory.toggle.assert_called_once()
