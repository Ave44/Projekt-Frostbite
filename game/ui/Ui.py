from config import *
from game.CameraSpriteGroup import CameraSpriteGroup
from game.item.Item import Item
from game.ui.SelectedItem import SelectedItem
from game.ui.inventory.Inventory import Inventory


class Ui:
    def __init__(self, visibleSprites: CameraSpriteGroup, selectedItem: SelectedItem, playerPos: pygame.math.Vector2()):
        self.visibleSprites = visibleSprites
        self.selectedItem = selectedItem
        self.playerPos = playerPos
        self.windowOffset = (- WINDOW_WIDTH // 2, - WINDOW_HEIGHT // 2)
        self.inventory = Inventory(visibleSprites, 5, 4, self.calculateUiPos(), selectedItem)

    def handleMouseLeftClick(self) -> None:
        calculatedMousePos = self.getCalculatedMousePos()
        self.inventory.handleMouseLeftClick(calculatedMousePos)

    def handleMouseRightClick(self) -> None:
        calculatedMousePos = self.getCalculatedMousePos()
        self.inventory.handleMouseRightClick(calculatedMousePos)

    def toggleInventory(self) -> None:
        self.inventory.toggle()
        self.visibleSprites.remove(self.selectedItem)
        self.visibleSprites.add(self.selectedItem)

    def update(self, newPlayerPos: pygame.math.Vector2()) -> None:
        self.playerPos = newPlayerPos
        self.inventory.changePos(self.calculateUiPos())

        if not self.selectedItem.isEmpty():
            calculatedMousePos = self.getCalculatedMousePos()
            self.selectedItem.updatePos(calculatedMousePos)
            return

    def calculateUiPos(self) -> pygame.math.Vector2():
        return (self.playerPos[0] + self.windowOffset[0],
                self.playerPos[1] + self.windowOffset[1])

    def getCalculatedMousePos(self) -> pygame.math.Vector2():
        mousePos = pygame.mouse.get_pos()
        uiPos = self.calculateUiPos()
        calculatedMousePos = (mousePos[0] + uiPos[0],
                              mousePos[1] + uiPos[1])
        return calculatedMousePos
