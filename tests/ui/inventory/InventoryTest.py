import unittest

from mock.mock import MagicMock, Mock
from pygame.math import Vector2

from game.entities.Player import Player
from game.ui.inventory.Inventory import Inventory
from game.ui.inventory.slot.Slot import Slot
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.items.Item import Item
from game.ui.inventory.slot.SelectedItem import SelectedItem


class InventoryTest(unittest.TestCase):

    def setUp(self) -> None:
        visibleSprites = CameraSpriteGroup()
        self.playerPos = (34, 15)
        self.emptyInventory = Inventory(visibleSprites, 1, 2, Vector2(0, 0))
        self.fullInventory = Inventory(visibleSprites, 0, 0, Vector2(0, 0))
        self.item = Item(visibleSprites, Vector2())
        self.fullInventoryWithSelectedItem = Inventory(visibleSprites, 0, 0, Vector2(self.playerPos))
        self.newPlayerPos = (3, 4)

        self.emptyInventory.toggle()
        self.fullInventory.toggle()
        self.fullInventoryWithSelectedItem.toggle()

        self.player = MagicMock(Player)

    def test_inventoryList_should_has_correct_length(self):
        self.assertEqual(2, len(self.emptyInventory.slotList))

    def test_isOpen_should_be_True_used_on_open_inventory(self):
        self.assertEqual(True, self.emptyInventory.isOpen)

    def test_toggle_should_close_open_inventory(self):
        self.emptyInventory.toggle()
        self.assertEqual(False, self.emptyInventory.isOpen)

    def test_2x_toggle_should_open_closed_inventory(self):
        self.emptyInventory.toggle()
        self.emptyInventory.toggle()
        self.assertEqual(True, self.emptyInventory.isOpen)

    def test_set_inventoryList_should_change_inventoryList_when_called_with_the_same_length_list(self):
        newInventoryList = [Slot(Vector2(0, 0)), Slot(Vector2(0, 0))]
        self.emptyInventory.inventoryList = newInventoryList
        self.assertEqual(newInventoryList, self.emptyInventory.inventoryList)

    def test_addItem_should_addItem_to_empty_slot_in_inventory_with_empty_slot(self):
        selectedItem = SelectedItem(self.player)
        self.emptyInventory.addItem(self.item, selectedItem)
        self.assertEqual(self.item, self.emptyInventory.slotList[0].item)

    def test_addItem_should_add_to_selectedItem_in_full_inventory_with_empty_selectedItem(self):
        selectedItem = SelectedItem(self.player)
        self.fullInventory.addItem(self.item, selectedItem)
        self.assertEqual(self.item, selectedItem.item)


if __name__ == '__main__':
    unittest.main()
