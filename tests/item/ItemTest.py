import os.path
import unittest

import pygame.sprite
from pygame import Vector2

from config import ROOT_PATH
from game.items.Item import Item


class ItemTest(unittest.TestCase):

    def setUp(self) -> None:
        self.item = Item(pygame.sprite.Group(), Vector2())

    def test_id_should_be_different(self):
        item2 = Item(pygame.sprite.Group(), Vector2())
        self.assertNotEqual(self.item.id, item2.id)

    def test_drop_should_change_item_pos(self):
        self.item.drop((1, 2))
        self.assertEqual((1, 2), self.item.rect.center)


if __name__ == '__main__':
    unittest.main()
