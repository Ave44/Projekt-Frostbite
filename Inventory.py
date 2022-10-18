from Item import Item
from Slot import Slot


class Inventory:
    def __init__(self, size: int):
        self.inventoryArray: list[Slot] = [Slot()] * size
        self.size: int = size

    def addItem(self, item: Item) -> None:
        first: Slot | None = next(filter(lambda slot: (slot.isEmpty()), self.inventoryArray), None)
        if first is None:
            raise ValueError("The inventroy is full")
        else:
            indexOfSlot: int = self.inventoryArray.index(first)
            self.inventoryArray[indexOfSlot].item = item

    def deleteItem(self, index: int) -> None:
        if index >= self.size:
            raise ValueError("Index out of range")
        self.inventoryArray[index].dropItem()

    def findAndDeleteItem(self, item: Item) -> None:
        first: Slot | None = next(filter(lambda slot: (slot.item is item), self.inventoryArray), None)
        if first is None:
            raise ValueError("Can not find the item")
        else:
            indexOfSlot: int = self.inventoryArray.index(first)
            self.inventoryArray[indexOfSlot].dropItem()

    def enlargeInventroy(self, newInventorySize: int) -> None:
        if newInventorySize <= self.size:
            raise ValueError("You have to enlare for a 1 or more slots")
        self.inventoryArray += [Slot()] * (newInventorySize - self.size)
        self.size = newInventorySize

    def reduceInventory(self, newInventorySize: int) -> None:
        if newInventorySize >= self.size:
            raise ValueError("You have to reduce for a 1 or more slots")
        self.inventoryArray = self.inventoryArray[:self.size - newInventorySize]
        self.size = newInventorySize
