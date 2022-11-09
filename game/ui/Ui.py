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
        self.inventory = Inventory(visibleSprites, 5, 4, self.__calculateUiPos(), selectedItem)

    def handleMouseLeftClick(self) -> None:
        calculatedMousePos = self.__getCalculatedMousePos()
        self.inventory.handleMouseLeftClick(calculatedMousePos)

    def handleMouseRightClick(self) -> None:
        calculatedMousePos = self.__getCalculatedMousePos()
        self.inventory.handleMouseRightClick(calculatedMousePos)

    def toggleInventory(self) -> None:
        self.inventory.toggle()
        self.visibleSprites.remove(self.selectedItem)
        self.visibleSprites.add(self.selectedItem)

    def update(self, newPlayerPos: tuple[int, int]) -> None:
        self._playerPos = newPlayerPos
        self.inventory.changePos(self.__calculateUiPos())

        if not self.selectedItem.isEmpty():
            calculatedMousePos = self.__getCalculatedMousePos()
            self.selectedItem.updatePos(calculatedMousePos)
            return

    def __calculateUiPos(self) -> tuple[int, int]:
        return (self._playerPos[0] + self._windowOffset[0],
                self._playerPos[1] + self._windowOffset[1])

    def __getCalculatedMousePos(self) -> tuple[int, int]:
        mousePos = pygame.mouse.get_pos()
        uiPos = self.__calculateUiPos()
        calculatedMousePos = (mousePos[0] + uiPos[0],
                              mousePos[1] + uiPos[1])
        return calculatedMousePos
