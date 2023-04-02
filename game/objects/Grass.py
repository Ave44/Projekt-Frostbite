from pygame.math import Vector2
from pygame.time import Clock
from pygame.sprite import Group
from game.LoadedImages import LoadedImages

from game.items.Sword import Sword
from game.items.domain.ToolType import ToolType
from game.objects.domain.Object import Object
from game.objects.domain.AnimatedObject import AnimatedObject


class Grass(Object, AnimatedObject):
    def __init__(self, visibleGroup: Group, midBottom: Vector2, loadedImages: LoadedImages, clock: Clock):
        image = loadedImages.grass[0]
        Object.__init__(self, visibleGroup,
                         midBottom, 1, ToolType.SHOVEL, image)
        AnimatedObject.__init__(self, loadedImages.grass, clock, 120)

    def interact(self) -> None:
        # do something
        pass

    def drop(self) -> None:
        Sword(self.visibleGroup, self.rect.midBottom)

    def update(self) -> None:
        AnimatedObject.animationUpdate(self)
