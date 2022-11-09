import os.path
import unittest

from config import ROOT_PATH
from game.item.Item import Item


class ItemTest(unittest.TestCase):

    def setUp(self) -> None:
        self.item = Item("sword")

    def test_id_should_be_different(self):
        item2 = Item("another sword", os.path.join(ROOT_PATH, "graphics", "items", "sword.png"))
        self.assertNotEqual(self.item.id, item2.id)

    def test_drop_should_change_item_pos(self):
        self.item.drop((1, 2))
        self.assertEqual((1, 2), self.item.rect.center)


if __name__ == '__main__':
    unittest.main()