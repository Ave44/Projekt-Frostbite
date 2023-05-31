import unittest
from unittest import TestCase

from unittest.mock import MagicMock, Mock

from pygame import Surface
from pygame.math import Vector2
from pygame.sprite import Group

from game.LoadedImages import LoadedImages
from game.entities.Player import Player
from game.items.domain.Item import Item
from game.ui.inventory.Inventory import Inventory
from game.ui.inventory.slot.SelectedItem import SelectedItem
from game.ui.inventory.slot.Slot import Slot


class InventoryTest(TestCase):

    def setUp(self) -> None:
        visibleSprites = Group()
        self.item = Mock(Item)
        self.playerPos = (34, 15)
        self.loadedImages = Mock(LoadedImages)
        self.loadedImages.slot = Surface((0, 0))
        self.emptySelectedItem = Mock(SelectedItem)
        self.emptySelectedItem.isEmpty = Mock(return_value=True)
        self.emptySelectedItem.item = None
        self.emptyInventory = Inventory(visibleSprites, 1, 2, Vector2(0, 0), self.loadedImages)
        self.emptyInventory.slotList = [Mock(Slot), Mock(Slot)]
        self.emptyInventory.slotList[0].getItemId = Mock(return_value="1")
        self.emptyInventory.slotList[1].getItemId = Mock(return_value="2")
        self.fullInventory = Inventory(visibleSprites, 0, 0, Vector2(0, 0), self.loadedImages)
        self.fullInventoryWithSelectedItem = Inventory(visibleSprites, 0, 0, Vector2(self.playerPos), self.loadedImages)
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

    def test_addItem_should_call_addItem_on_first_empty_slot(self):
        self.emptyInventory.addItem(self.item, self.emptySelectedItem)
        self.emptyInventory.slotList[0].addItem.assert_called_once()

    def test_addItem_should_call_addItem_on_selectedItem_when_inventory_is_full(self):
        self.fullInventory.addItem(self.item, self.emptySelectedItem)
        self.emptySelectedItem.addItem.assert_called_once()

    def test_getSaveData_should_return_itemId_of_every_item(self):
        saveData = self.emptyInventory.getSaveData()
        self.assertIn('slotsItemData', saveData)
        self.assertEqual(saveData['slotsItemData'], ["1", "2"])


if __name__ == '__main__':
    unittest.main()