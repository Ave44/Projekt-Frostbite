from config import *
from game.CameraSpriteGroup import CameraSpriteGroup
from game.item.Item import Item
from game.ui.SelectedItem import SelectedItem
from game.ui.inventory.Inventory import Inventory


class Ui:
    def __init__(self, visibleSprites: CameraSpriteGroup, selectedItem: SelectedItem, playerPos: tuple[int, int]):
        self.visibleSprites = visibleSprites
        self.selectedItem = selectedItem
        self._playerPos = playerPos
        self._windowOffset = (- WINDOW_WIDTH // 2, - WINDOW_HEIGHT // 2)
        self._inventory = Inventory(visibleSprites, 5, 4, self.__calculateUiPos(), selectedItem)
        self._inventory.addItem(Item("sword"))
        self._inventory.addItem(Item("sword", "sword.png", "sword.png"))

    def handleMouseLeftClick(self):
        calculatedMousePos = self.__getCalculatedMousePos()
        self._inventory.handleMouseLeftClick(calculatedMousePos)

    def handleMouseRightClick(self):
        calculatedMousePos = self.__getCalculatedMousePos()
        self._inventory.handleMouseRightClick(calculatedMousePos)

    def toggleInventory(self):
        self._inventory.toggle()
        self.visibleSprites.remove(self.selectedItem)
        self.visibleSprites.add(self.selectedItem)

    def update(self, newPlayerPos: tuple[int, int]) -> None:
        self._playerPos = newPlayerPos
        self._inventory.changePos(self.__calculateUiPos())

        if self.selectedItem.isEmpty():
            return
        calculatedMousePos = self.__getCalculatedMousePos()
        self.selectedItem.updatePos(calculatedMousePos)
        return

    def __calculateUiPos(self):
        return (self._playerPos[0] + self._windowOffset[0],
                self._playerPos[1] + self._windowOffset[1])

    def __getCalculatedMousePos(self):
        mousePos = pygame.mouse.get_pos()
        uiPos = self.__calculateUiPos()
        calculatedMousePos = (mousePos[0] + uiPos[0],
                              mousePos[1] + uiPos[1])
        return calculatedMousePos
