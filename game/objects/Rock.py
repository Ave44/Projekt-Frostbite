from pygame import Rect
from pygame.math import Vector2
from pygame.sprite import Group
from game.LoadedImages import LoadedImages

from game.items.Pebble import Pebble
from game.items.SharpRock import SharpRock
from game.items.domain.Pickaxe import Pickaxe
from game.objects.domain.CollisionObject import CollisionObject


class Rock(CollisionObject):
    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, midBottom: Vector2, loadedImages: LoadedImages):
        self.loadedImages = loadedImages
        image = loadedImages.rock
        colliderRect = Rect((0, 0), (10, 10))
        colliderRect.midbottom = midBottom

        CollisionObject.__init__(self, visibleGroup, obstaclesGroup, midBottom, 10, Pickaxe, image, colliderRect)

    def interact(self) -> None:
        # do something
        pass

    def drop(self) -> None:
        Pebble(self.visibleGroup, self.rect.center, self.loadedImages)
        Pebble(self.visibleGroup, self.rect.center, self.loadedImages)
        SharpRock(self.visibleGroup, self.rect.center, self.loadedImages)
