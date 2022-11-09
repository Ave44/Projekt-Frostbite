import unittest

from mock.mock import Mock

from game.item.Item import Item
from game.ui.inventory.Slot import Slot


class SlotTest(unittest.TestCase):

    def setUp(self) -> None:
        self.item = Item("Icon")
        self.emptySlot = Slot((0, 0))
        self.slot = Slot((0, 0), self.item)

    def test_isEmpty_should_return_True_when_called_on_empty_slot(self):
        self.assertEqual(True, self.emptySlot.isEmpty())

    def test_isEmpty_should_return_False_when_called_on_not_empty_slot(self):
        self.assertEqual(False, self.slot.isEmpty())

    def test_addItem_should_add_item_when_called_on_empty_slot(self):
        self.emptySlot.addItem(self.item)
        self.assertEqual(self.item, self.emptySlot.item)

    def test_addItem_should_raise_error_when_called_on_not_empty_slot(self):
        with self.assertRaises(ValueError):
            self.slot.addItem(self.item)

    def test_removeItem_should_remove_item_when_called_on_not_empty_slot(self):
        self.slot.removeItem()
        self.assertEqual(None, self.emptySlot.item)

    def test_removeItem_should_raise_error_when_called_on_empty_slot(self):
        with self.assertRaises(ValueError):
            self.emptySlot.removeItem()

    def test_use_should_use_item_when_called_on_not_empty_slot(self):
        item = Mock()
        self.emptySlot.item = item
        self.emptySlot.use()

        item.use.assert_called_once()

    def test_use_should_raise_error_when_called_on_empty_slot(self):
        with self.assertRaises(ValueError):
            self.emptySlot.use()


if __name__ == '__main__':
    unittest.main()
