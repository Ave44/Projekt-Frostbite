import unittest

import mock

from config import *
from game.CameraSpriteGroup import CameraSpriteGroup
from ui.inventory.items.SelectedItem import SelectedItem
from game.ui.Ui import Ui


class UiTest(unittest.TestCase):

    def setUp(self) -> None:
        visibleSprite = CameraSpriteGroup()
        self.playerPos = (3, 56)
        self.ui = Ui(visibleSprite, SelectedItem(self.playerPos), self.playerPos)

    @mock.patch("pygame.mouse")
    @mock.patch("game.ui.inventory.Inventory")
    def test_handleMouseLeftClick_should_call_inventory_handleMouseLeftClick_once(self, _, mockInventory):
        self.ui.inventory = mockInventory
        self.ui.handleMouseLeftClick()

        mockInventory.handleMouseLeftClick.assert_called_once()

    @mock.patch("pygame.mouse")
    @mock.patch("game.ui.inventory.Inventory")
    def test_handleMouseRightClick_should_call_inventory_handleMouseRightClick_once(self, _, mockInventory):
        self.ui.inventory = mockInventory
        self.ui.handleMouseRightClick()

        mockInventory.handleMouseRightClick.assert_called_once()

    @mock.patch("game.ui.inventory.Inventory")
    def test_toggleInventory_should_call_toggle_on_inventory_once(self, mockInventory):
        self.ui.inventory = mockInventory
        self.ui.toggleInventory()

        mockInventory.toggle.assert_called_once()

    @mock.patch("game.ui.inventory.Inventory")
    def test_update_should_call_inventory_changePos_once(self, mockInventory):
        self.ui.inventory = mockInventory
        self.ui.update((1, 1))

        mockInventory.changePos.assert_called_once()

    @mock.patch("game.ui.inventory.Inventory")
    def test_update_should_call_inventory_changePos_with_correct_value(self, mockInventory):
        self.ui.inventory = mockInventory
        newPlayerPos = (1, 1)

        self.ui.update(newPlayerPos)

        uiPos = (- WINDOW_WIDTH // 2 + newPlayerPos[0], - WINDOW_HEIGHT // 2 + newPlayerPos[1])

        mockInventory.changePos.assert_called_with(uiPos)

    @mock.patch("pygame.mouse")
    @mock.patch("game.ui.SelectedItem")
    def test_update_should_update_selectedItem_pos_when_selectedItem_not_empty(self, _, mockSelectedItem):
        mockSelectedItem.isEmpty.return_value = False

        self.ui.selectedItem = mockSelectedItem
        self.ui.update((1, 1))

        mockSelectedItem.updatePos.assert_called_once()
