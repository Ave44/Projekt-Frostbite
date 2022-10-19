from Item import Item


class Slot:
    def __init__(self, item: Item = None):
        self._item = item

    @property
    def item(self) -> Item:
        if self.isEmpty():
            raise ValueError("The slot is empty")
        else:
            return self._item

    @item.setter
    def item(self, item: Item) -> None:
        self._item = item

    def isEmpty(self) -> bool:
        if self.item is None:
            return False
        else:
            return True

    def dropItem(self) -> None:
        self._item = None
