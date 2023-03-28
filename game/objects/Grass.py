from pygame.math import Vector2
from pygame.sprite import Group

from game.items.Sword import Sword
from game.items.domain.ToolType import ToolType
from game.objects.domain.Object import Object


class Grass(Object):
    def __init__(self, visibleGroup: Group, midBottom: Vector2, loadedImages: list):
        self.loadedImages = loadedImages
        image = loadedImages.grass[0]
        super().__init__(visibleGroup,
                         midBottom, 1, ToolType.SHOVEL, image)

    def interact(self) -> None:
        # do something
        pass

    def drop(self) -> None:
        Sword(self.visibleGroup, self.rect.midBottom)
