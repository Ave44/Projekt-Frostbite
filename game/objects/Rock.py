from pygame import Rect
from pygame.math import Vector2
from pygame.sprite import Group
from game.LoadedImages import LoadedImages

from game.items.Pebble import Pebble
from game.items.SharpRock import SharpRock
from game.items.domain.Pickaxe import Pickaxe
from game.objects.domain.CollisionObject import CollisionObject


class Rock(CollisionObject):
    def __init__(self, visibleSprites: Group, obstacleSprites: Group, midbottom: Vector2, loadedImages: LoadedImages, currentDurability: int = None):
        self.loadedImages = loadedImages
        image = loadedImages.rock
        colliderRect = Rect((0, 0), (30, 15))
        colliderRect.midbottom = midbottom

        CollisionObject.__init__(self, visibleSprites, obstacleSprites, midbottom, 10, Pickaxe, image, colliderRect, currentDurability)

    def interact(self) -> None:
        # do something
        pass

    def drop(self) -> None:
        Pebble(self.visibleSprites, self.rect.center, self.loadedImages)
        Pebble(self.visibleSprites, self.rect.center, self.loadedImages)
        SharpRock(self.visibleSprites, self.rect.center, self.loadedImages)
