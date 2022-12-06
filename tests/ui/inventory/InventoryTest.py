import unittest

import pygame
from mock.mock import MagicMock

from entities.Player import Player
from game.ui.inventory.Inventory import Inventory
from game.ui.inventory.Slot import Slot
from spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from ui.inventory.items.Item import Item
from ui.inventory.state.SelectedItem import SelectedItem


class InventoryTest(unittest.TestCase):

    def setUp(self) -> None:
        visibleSprites = CameraSpriteGroup()
        self.playerPos = (34, 15)
        self.emptyInventory = Inventory(visibleSprites, 1, 2, (0, 0))
        self.fullInventory = Inventory(visibleSprites, 0, 0, (0, 0))
        self.item = Item(visibleSprites, pygame.math.Vector2())
        self.fullInventoryWithSelectedItem = Inventory(visibleSprites, 0, 0, self.playerPos)
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

    def test_set_inventoryList_should_raise_error_when_called_with_different_length_list(self):
        with self.assertRaises(ValueError):
            self.fullInventory.inventoryList = [Slot((0, 0))]

    def test_set_inventoryList_should_change_inventoryList_when_called_with_the_same_length_list(self):
        newInventoryList = [Slot((0, 0)), Slot((0, 0))]
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

    def test_addItem_should_set_newItem_as_selectedItem_in_full_inventory_with_selectedItem(self):
        newItem = Item("axe")
        self.fullInventoryWithSelectedItem.addItem(newItem)

        self.assertEqual(newItem, self.fullInventoryWithSelectedItem.selectedItem)

    def test_addItem_should_drop_oldItem_on_player_pos_in_full_inventory_with_selectedItem(self):
        oldItem = self.fullInventoryWithSelectedItem.selectedItem.item
        self.fullInventoryWithSelectedItem.addItem(Item("sword"))

        self.assertEqual(self.playerPos, oldItem.rect.center)

    def test_changePos_should_change_slot_rect(self):
        oldSlotRect = self.emptyInventory.inventoryList[0].rect.center
        self.emptyInventory.changePos(self.newPlayerPos)
        newSlotRect = self.emptyInventory.inventoryList[0].rect.center

        self.assertEqual(self.newPlayerPos, (newSlotRect[0] - oldSlotRect[0], newSlotRect[1] - oldSlotRect[1]))

    def test_changePos_should_change_inventory_pos(self):
        newCenter = (312, 4)

        self.emptyInventory.changePos(newCenter)

        # center = (self.emptyInventory.rect.center[0] - self.p)

        self.assertEqual(newCenter, self.emptyInventory.rect.topleft)

    def test_handleMouseLeftClick_should_drop_selectedItem_when_cursor_outside_inventory_with_selectedItem(self):
        itemBeforeDrop = self.fullInventoryWithSelectedItem.selectedItem.item
        self.fullInventoryWithSelectedItem.handleMouseLeftClick((600, 500))

        self.assertEqual(self.playerPos, itemBeforeDrop.rect.center)
        self.assertEqual(None, self.fullInventoryWithSelectedItem.selectedItem.item)

    def test_handleMouseLeftClick_should_drop_selectedItem_when_inventory_closed_cursor_over_inventory(self):
        self.emptyInventory.toggle()
        self.emptyInventory.selectedItem.item = Item("sword2")

        itemBeforeDrop = self.emptyInventory.selectedItem.item

        emptySlot = self.emptyInventory.inventoryList[0]
        self.emptyInventory.handleMouseLeftClick(emptySlot.rect.center)

        self.assertEqual(self.playerPos, itemBeforeDrop.rect.center)
        self.assertEqual(None, self.emptyInventory.selectedItem.item)

    def test_handleMouseRightClick_should_use_hovered_slot_when_hover_and_not_selected_item(self):
        firstSlot = MagicMock()
        firstSlot.rect.center.return_value = self.emptyInventory.inventoryList[0].rect.center

        self.emptyInventory.inventoryList = [firstSlot, Slot((1, 1))]

        self.emptyInventory.handleMouseRightClick(firstSlot.rect.center)
        firstSlot.use.assert_called_once()

    def test_update_should_move_selectedItem_when_hover_outside_inventory_and_not_clicked_mouse1(self):
        itemRectBeforeMove = self.fullInventoryWithSelectedItem.selectedItem.rect[:]
        newItemPos = (itemRectBeforeMove[0] + 1000, itemRectBeforeMove[1] + 2000)

        self.fullInventoryWithSelectedItem.update()
        self.assertNotEqual(newItemPos, self.fullInventoryWithSelectedItem.selectedItem.rect)

    def test_handleMouseLeftClick_should_place_selectedItem_when_hover_over_empty_slot(self):
        emptySlot = self.emptyInventory.inventoryList[0]
        item = Item("sword")
        self.emptyInventory.selectedItem.item = item

        self.emptyInventory.handleMouseLeftClick(emptySlot.rect.center)
        self.assertEqual(item, emptySlot.item)
        self.assertEqual(None, self.emptyInventory.selectedItem.item)

    def test_handleMouseLeftClick_should_swap_items_when_hover_over_not_empty_slot_with_selectedItem(self):
        oldItem = Item("sword")
        self.emptyInventory.addItem(oldItem)
        notEmptySlot = self.emptyInventory.inventoryList[0]

        newItem = Item("new sword")
        self.emptyInventory.selectedItem.item = newItem
        self.emptyInventory.handleMouseLeftClick(notEmptySlot.rect.center)

        self.assertEqual(newItem, notEmptySlot.item)
        self.assertEqual(oldItem, self.emptyInventory.selectedItem.item)


if __name__ == '__main__':
    unittest.main()
