import unittest

from mock.mock import Mock
from pygame import Vector2

from game.ui.inventory.slot.Slot import Slot
from game.items.Item import Item


class SlotTest(unittest.TestCase):

    def setUp(self) -> None:
        self.item = Mock(Item)
        self.emptySlot = Slot(Vector2(0, 0))
        self.slot = Slot(Vector2(0, 0), self.item)

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

    def test_use_should_use_item_when_called_on_not_empty_slot(self):
        item = Mock()
        self.emptySlot.item = item
        self.emptySlot.use()

        item.use.assert_called_once()


if __name__ == '__main__':
    unittest.main()
