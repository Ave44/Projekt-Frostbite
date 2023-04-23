from pygame import Rect
from pygame.math import Vector2
from pygame.sprite import Group
from game.LoadedImages import LoadedImages

from game.items.domain.Item import Item
from game.items.domain.Axe import Axe
from game.objects.domain.CollisionObject import CollisionObject


class BurntTree(CollisionObject):
    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, midBottom: Vector2, loadedImages: LoadedImages):
        self.loadedImages = loadedImages
        image = loadedImages.burntTree
        colliderRect = Rect((0, 0), (5, 5))
        colliderRect.midbottom = midBottom
        CollisionObject.__init__(self, visibleGroup, obstaclesGroup,
                                 midBottom, 1, Axe, image, colliderRect)

    def interact(self) -> None:
        print("interacted with burnt trees")  # in the future there will be a real implementation

    def drop(self) -> None:
        Item(self.visibleGroup, self.rect.center)  # in the future there will be a real implementation
