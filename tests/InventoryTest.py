import unittest

from mock import mock
from mock.mock import MagicMock


from game.CameraSpriteGroup import CameraSpriteGroup
from game.Inventory import Inventory
from game.Item import Item
from game.Slot import Slot


class InventoryTest(unittest.TestCase):

    def setUp(self) -> None:
        visibleSprites = CameraSpriteGroup()
        self.emptyInventory = Inventory(visibleSprites, 1, 2, (0, 0))
        self.fullInventory = Inventory(visibleSprites, 0, 0, (0, 0))
        self.item = Item("sword")
        self.fullInventoryWithSelectedItem = Inventory(visibleSprites, 0, 0, (3, 2), self.item)
        self.newPlayerPos = (3, 4)

    def test_inventoryList_should_has_correct_length(self):
        self.assertEqual(2, len(self.emptyInventory.inventoryList))

    def test_isOpen_should_be_False_used_on_closed_inventory(self):
        self.assertEqual(False, self.emptyInventory.isOpen)

    def test_toggle_should_open_closed_inventory(self):
        self.emptyInventory.toggle()
        self.assertEqual(True, self.emptyInventory.isOpen)

    def test_2x_toggle_should_open_closed_inventory(self):
        self.emptyInventory.toggle()
        self.emptyInventory.toggle()
        self.assertEqual(False, self.emptyInventory.isOpen)

    def test_set_inventoryList_should_raise_error_when_called_with_different_length_list(self):
        with self.assertRaises(ValueError):
            self.fullInventory.inventoryList = [Slot((0, 0))]

    def test_set_inventoryList_should_change_inventoryList_when_called_with_the_same_length_list(self):
        newInventoryList = [Slot((0, 0)), Slot((0, 0))]
        self.emptyInventory.inventoryList = newInventoryList
        self.assertEqual(newInventoryList, self.emptyInventory.inventoryList)

    def test_addItem_should_addItem_to_empty_slot_in_inventory_with_empty_slot(self):
        self.emptyInventory.addItem(self.item)
        self.assertEqual(self.item, self.emptyInventory.inventoryList[0].item)

    def test_addItem_should_add_to_selectedItem_in_full_inventory_with_empty_selectedItem(self):
        self.fullInventory.addItem(self.item)
        self.assertEqual(self.item, self.fullInventory.selectedItem)

    def test_addItem_should_set_newItem_as_selectedItem_in_full_inventory_with_selectedItem(self):
        newItem = Item("axe")
        self.fullInventoryWithSelectedItem.addItem(newItem)

        self.assertEqual(newItem, self.fullInventoryWithSelectedItem.selectedItem)

    def test_addItem_should_drop_oldItem_on_player_pos_in_full_inventory_with_selectedItem(self):
        oldItem = self.fullInventoryWithSelectedItem.selectedItem
        self.fullInventoryWithSelectedItem.addItem(Item("sword"))

        self.assertEqual(self.fullInventoryWithSelectedItem.playerPos, oldItem.rect.center)

    def test_updatePos_should_update_playerPos_value(self):
        self.emptyInventory.updatePos(self.newPlayerPos)
        self.assertEqual(self.newPlayerPos, self.emptyInventory.playerPos)

    def test_updatePos_should_update_totalOffset_value(self):
        oldTotalOffset = self.emptyInventory.totalOffset
        self.emptyInventory.updatePos(self.newPlayerPos)
        newTotalOffset = self.emptyInventory.totalOffset

        actual = (newTotalOffset[0] - oldTotalOffset[0], newTotalOffset[1] - oldTotalOffset[1])
        self.assertEqual(self.newPlayerPos, actual)

    def test_updatePos_should_change_slot_rect(self):
        oldSlotRect = self.emptyInventory.inventoryList[0].rect.center
        self.emptyInventory.updatePos(self.newPlayerPos)
        newSlotRect = self.emptyInventory.inventoryList[0].rect.center

        self.assertEqual(self.newPlayerPos, (newSlotRect[0] - oldSlotRect[0], newSlotRect[1] - oldSlotRect[1]))

    @mock.patch('pygame.mouse')
    def test_handleMouseLeftClick_should_drop_selectedItem_when_cursor_outside_inventory_with_selectedItem(self, mouse):
        mouse.get_pressed.return_value = (True, False, False)
        mouse.get_pos.return_value = (200, 500)

        itemBeforeDrop = self.fullInventoryWithSelectedItem.selectedItem
        self.fullInventoryWithSelectedItem.handleMouseLeftClick()

        self.assertEqual((3, 2), itemBeforeDrop.rect.center)
        self.assertEqual(None, self.fullInventoryWithSelectedItem.selectedItem)

    @mock.patch('pygame.mouse')
    def test_update_should_move_selectedItem_when_slot_hover_selectedItem_and_not_clicked_mouse1(self, mouse):
        itemRectBeforeMove = self.fullInventoryWithSelectedItem.selectedItem.rect[:]
        newItemPos = (itemRectBeforeMove[0] + 1, itemRectBeforeMove[1] + 2)

        mouse.get_pressed.return_value = (False, False, False)
        mouse.get_pos.return_value = newItemPos

        self.fullInventoryWithSelectedItem.update()
        self.assertNotEqual(newItemPos, self.fullInventoryWithSelectedItem.selectedItem.rect)

    @mock.patch('pygame.mouse')
    def test_handleMouseRightClick_should_use_hovered_slot_when_hover_and_not_selected_item(self, mouse):
        firstSlot = MagicMock()
        firstSlot.rect.center.return_value = self.emptyInventory.inventoryList[0].rect.center

        self.emptyInventory.inventoryList = [firstSlot, Slot((1, 1))]

        mouse.get_pressed.return_value = (False, True, False)
        mouse.get_pos.return_value = (firstSlot.rect.center[0] - self.emptyInventory.totalOffset[0],
                                      firstSlot.rect.center[1] - self.emptyInventory.totalOffset[1])

        self.emptyInventory.handleMouseRightClick()
        firstSlot.use.assert_called_once()

    @mock.patch('pygame.mouse')
    def test_update_should_move_selectedItem_when_hover_outside_inventory_and_not_clicked_mouse1(self, mouse):
        itemRectBeforeMove = self.fullInventoryWithSelectedItem.selectedItem.rect[:]
        newItemPos = (itemRectBeforeMove[0] + 1000, itemRectBeforeMove[1] + 2000)

        mouse.get_pressed.return_value = (False, False, False)
        mouse.get_pos.return_value = newItemPos

        self.fullInventoryWithSelectedItem.update()
        self.assertNotEqual(newItemPos, self.fullInventoryWithSelectedItem.selectedItem.rect)

    @mock.patch('pygame.mouse')
    def test_handleMouseLeftClick_should_place_selectedItem_when_hover_over_empty_slot(self, mouse):
        emptySlot = self.emptyInventory.inventoryList[0]
        item = Item("sword")
        self.emptyInventory.selectedItem = item

        mouse.get_pressed.return_value = (True, False, False)
        mouse.get_pos.return_value = (emptySlot.rect.center[0] - self.emptyInventory.totalOffset[0],
                                      emptySlot.rect.center[1] - self.emptyInventory.totalOffset[1])

        self.emptyInventory.handleMouseLeftClick()
        self.assertEqual(item, emptySlot.item)
        self.assertEqual(None, self.emptyInventory.selectedItem)

    @mock.patch('pygame.mouse')
    def test_handleMouseLeftClick_should_swap_items_when_hover_over_not_empty_slot_with_selectedItem(self, mouse):
        oldItem = Item("sword")
        self.emptyInventory.addItem(oldItem)
        notEmptySlot = self.emptyInventory.inventoryList[0]

        mouse.get_pressed.return_value = (True, False, False)
        mouse.get_pos.return_value = (notEmptySlot.rect.center[0] - self.emptyInventory.totalOffset[0],
                                      notEmptySlot.rect.center[1] - self.emptyInventory.totalOffset[1])

        newItem = Item("new sword")
        self.emptyInventory.selectedItem = newItem
        self.emptyInventory.handleMouseLeftClick()

        self.assertEqual(newItem, notEmptySlot.item)
        self.assertEqual(oldItem, self.emptyInventory.selectedItem)


if __name__ == '__main__':
    unittest.main()
