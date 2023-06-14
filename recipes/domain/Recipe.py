from abc import ABC, abstractmethod
from typing import Type

from game.items.domain.Item import Item


class Recipe(ABC):
    @property
    @abstractmethod
    def requiredItems(self) -> list[Type[Item]]:
        pass
