from game.CameraSpriteGroup import CameraSpriteGroup
from game.ui.inventory.Inventory import Inventory
from game.ui.UiInterface import UiInterface


class Ui(UiInterface):
    def __init__(self, visibleSprites: CameraSpriteGroup, playerPos: tuple[int, int]):
        self._playerPos = playerPos
        self._inventory = Inventory(visibleSprites, 5, 4, playerPos)

    def handleMouseLeftClick(self):
        self._inventory.handleMouseLeftClick()

    def handleMouseRightClick(self):
        self._inventory.handleMouseRightClick()
