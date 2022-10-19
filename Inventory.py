from Item import Item
from Slot import Slot


class Inventory:
    def __init__(self, size: int):
        self._inventoryList: list[Slot] = [Slot()] * size
        self._size: int = size

    @property
    def inventoryList(self) -> list[Slot]:
        return self._inventoryList

    @inventoryList.setter
    def inventoryList(self, newInventory: list[Slot]) -> None:
        self.inventoryList = newInventory

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, newSize: int) -> None:
        if newSize < self.size:
            self.inventoryList = self.inventoryList[:self.size - newSize]
            self.size = newSize
        else:
            self.inventoryList += [Slot()] * (newSize - self.size)
            self.size = newSize

    def addItem(self, item: Item) -> None:
        first: Slot | None = next(filter(lambda slot: (slot.isEmpty()), self.inventoryList), None)
        if first is None:
            raise ValueError("The inventroy is full")
        else:
            indexOfSlot: int = self.inventoryList.index(first)
            self.inventoryList[indexOfSlot].item = item

    def deleteItem(self, index: int) -> None:
        if index >= self.size:
            raise ValueError("Index out of range")
        self.inventoryList[index].dropItem()

    def findAndDeleteItem(self, item: Item) -> None:
        first: Slot | None = next(filter(lambda slot: (slot.item is item), self.inventoryList), None)
        if first is None:
            raise ValueError("Can not find the item")
        else:
            indexOfSlot: int = self.inventoryList.index(first)
            self.inventoryList[indexOfSlot].dropItem()
