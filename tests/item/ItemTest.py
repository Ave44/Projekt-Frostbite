import unittest
from unittest.mock import Mock

from pygame import Vector2, Surface
from pygame.sprite import Group

from game.LoadedImages import LoadedImages
from game.entities.Player import Player
from game.items.domain.Item import Item
from game.ui.inventory.Inventory import Inventory


class ItemTest(unittest.TestCase):
    def setUp(self) -> None:
        self.visibleSprites = Group()
        self.visibleSprites.items = Group()
        self.visibleSprites.savefileGroups = Group()
        self.visibleSprites.savefileGroups.Item = Group()
        self.loadedImages = Mock(LoadedImages)
        self.loadedImages.undefined = Surface((0, 0))

        self.item = Item(self.visibleSprites, Vector2(0, 0), self.loadedImages)
        self.item2 = Item(self.visibleSprites, Vector2(0, 0), self.loadedImages)

        self.player = Mock(Player)
        self.player.inventory = Mock(Inventory)
        self.player.selectedItem = self.item2

    def test_id_should_be_different_between_items(self):
        self.assertNotEqual(self.item.id, self.item2.id)

    def test_drop_should_change_item_pos(self):
        position = Vector2(1, 2)
        self.item.drop(position)
        self.assertEqual(position, self.item.rect.center)

    def test_drop_should_add_item_to_visibleSprites(self):
        self.item.drop(Vector2(0, 0))
        self.assertIn(self.item, self.visibleSprites)

    def test_getSaveData_should_return_dict_with_correct_item_pos(self):
        saveData = self.item.getSaveData()
        self.assertIn('center', saveData)
        self.assertEqual(saveData['center'], self.item.rect.center)

    def test_getSaveData_should_return_dict_with_correct_item_id(self):
        saveData = self.item.getSaveData()
        self.assertIn('id', saveData)
        self.assertEqual(saveData['id'], self.item.id)

    def test_onLeftClickAction_should_call_inventory_addItem(self):
        self.item.onLeftClickAction(self.player)
        self.player.inventory.addItem.assert_called_once()

if __name__ == '__main__':
    unittest.main()
