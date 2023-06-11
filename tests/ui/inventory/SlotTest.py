import unittest
from unittest.mock import Mock, MagicMock

from pygame import Vector2, Surface

from game.entities.Player import Player
from game.ui.inventory.slot.SelectedItem import SelectedItem
from game.ui.inventory.slot.Slot import Slot
from game.items.domain.Item import Item


class SlotTest(unittest.TestCase):
    def setUp(self) -> None:
        slotImage = Surface((0, 0))

        self.item = MagicMock(Item)
        self.item2 = MagicMock(Item)
        self.player = Mock(Player)
        self.player.selectedItem = Mock(SelectedItem)
        self.player.selectedItem.isEmpty = MagicMock(return_value = False)
        self.player.selectedItem.item = self.item2

        self.playerWithEmptySelectedItem = Mock(Player)
        self.playerWithEmptySelectedItem.selectedItem = Mock(SelectedItem)
        self.playerWithEmptySelectedItem.selectedItem.isEmpty = MagicMock(return_value = True)

        self.emptySlot = Slot(Vector2(0, 0), slotImage)
        self.slot = Slot(Vector2(0, 0), slotImage, self.item)

    def test_isEmpty_should_return_True_when_called_on_empty_slot(self):
        self.assertEqual(True, self.emptySlot.isEmpty())

    def test_isEmpty_should_return_False_when_called_on_not_empty_slot(self):
        self.assertEqual(False, self.slot.isEmpty())

    def test_addItem_should_add_item_when_called_on_empty_slot(self):
        self.emptySlot.addItem(self.item)
        self.assertEqual(self.item, self.emptySlot.item)

    def test_removeItem_should_remove_item_when_called_on_not_empty_slot(self):
        self.slot.removeItem()
        self.assertEqual(None, self.emptySlot.item)

    def test_handleMouseLeftClick_should_addItem_when_slot_is_empty_and_selectedItem_is_not(self):
        self.emptySlot.handleMouseLeftClick(self.player)
        self.assertEqual(self.item, self.slot.item)

    def test_handleMouseLeftClick_should_call_removeItem_method_on_selectedItem_when_slot_is_empty_and_selectedItem_is_not(self):
        self.emptySlot.handleMouseLeftClick(self.player)
        self.player.selectedItem.removeItem.assert_called_once()

    def test_handleMouseLeftClick_should_call_addItem_on_selectedItem_when_slot_is_not_empty_and_selectedItem_is(self):
        self.slot.handleMouseLeftClick(self.playerWithEmptySelectedItem)
        self.playerWithEmptySelectedItem.selectedItem.addItem.assert_called_once()

    def test_handleMouseLeftClick_should_removeItem_when_slot_is_not_empty_and_selectedItem_is(self):
        self.slot.handleMouseLeftClick(self.playerWithEmptySelectedItem)
        self.assertEqual(self.slot.item, None)

    def test_handleMouseLeftClick_swap_items_when_slot_and_selectedItem_is_not_empty(self):
        self.slot.handleMouseLeftClick(self.player)
        self.assertEqual(self.slot.item, self.item2)
        self.player.selectedItem.removeItem.assert_called_once()
        self.player.selectedItem.addItem.assert_called_once()

if __name__ == '__main__':
    unittest.main()
