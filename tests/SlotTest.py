import unittest

from game.Item import Item
from game.Slot import Slot


class SlotTest(unittest.TestCase):

    def setUp(self) -> None:
        self.item = Item("Icon")
        self.emptySlot = Slot((0, 0))
        self.slot = Slot((0, 0), self.item)

    def test_isEmpty_empty_slot(self):
        self.assertEqual(True, self.emptySlot.isEmpty())

    def test_isEmpty_not_empty_slot(self):
        self.assertEqual(False, self.slot.isEmpty())

    def test_addItem_on_empty_slot(self):
        self.emptySlot.addItem(self.item)
        self.assertEqual(self.item, self.emptySlot.item)

    def test_addItem_on_not_empty_slot(self):
        with self.assertRaises(ValueError):
            self.slot.addItem(self.item)

    def test_removeItem_on_not_empty_slot(self):
        self.slot.removeItem()
        self.assertEqual(None, self.emptySlot.item)

    def test_removeItem_on_empty_slot(self):
        with self.assertRaises(ValueError):
            self.emptySlot.removeItem()
