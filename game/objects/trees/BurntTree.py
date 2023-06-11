from pygame import Rect
from pygame.math import Vector2
from pygame.sprite import Group
from game.LoadedImages import LoadedImages

from game.items.Accorn import Accorn
from game.items.domain.Axe import Axe
from game.objects.domain.CollisionObject import CollisionObject


class BurntTree(CollisionObject):
    def __init__(self, visibleSprites: Group, obstacleSprites: Group, midbottom: Vector2, loadedImages: LoadedImages, currentDurability: int = None):
        self.loadedImages = loadedImages
        image = loadedImages.burntTree
        colliderRect = Rect((0, 0), (20, 20))
        colliderRect.midbottom = midbottom
        CollisionObject.__init__(self, visibleSprites, obstacleSprites,
                                 midbottom, 1, Axe, image, colliderRect, currentDurability)

    def interact(self) -> None:
        print("interacted with burnt trees")  # in the future there will be a real implementation

    def drop(self) -> None:
        Accorn(self.visibleSprites, self.rect.midbottom)  # in the future there will be a real implementation
