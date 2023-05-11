from pygame import Rect
from pygame.math import Vector2
from pygame.sprite import Group
from pygame.time import Clock
from game.LoadedImages import LoadedImages

from game.items.Wood import Wood
from game.items.Accorn import Accorn
from game.items.domain.Axe import Axe
from game.objects.domain.CollisionObject import CollisionObject
from game.objects.domain.Flammable import Flammable
from game.objects.trees.BurntTree import BurntTree
from game.objects.trees.Snag import Snag


class LargeTree(CollisionObject, Flammable):
    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, midBottom: Vector2,
                 loadedImages: LoadedImages, clock: Clock, ageMs: int = 0):
        self.loadedImages = loadedImages
        image = loadedImages.largeTree[0]
        colliderRect = Rect((0, 0), (20, 20))
        colliderRect.midbottom = midBottom

        CollisionObject.__init__(self, visibleGroup, obstaclesGroup,
                                 midBottom, 10, Axe, image, colliderRect)
        Flammable.__init__(self, clock)

        self.age = ageMs
        self.growthStage = 3
        self.LIFESPAN = 20000

    def interact(self) -> None:
        print("interacted with medium trees")  # in the future there will be a real implementation

    def drop(self) -> None:
        Wood(self.visibleGroup, self.rect.center, self.loadedImages)
        Wood(self.visibleGroup, self.rect.center, self.loadedImages)
        Wood(self.visibleGroup, self.rect.center, self.loadedImages)
        Accorn(self.visibleGroup, self.rect.center, self.loadedImages)

    def burn(self):
        self.remove(*self.groups())
        BurntTree(self.visibleGroup, self.obstaclesGroup, self.rect.midbottom, self.loadedImages)

    def update(self):
        if self.isOnFire and self.timeToBurn:
            self.flameUpdate()
            return
        self.age += self.clock.get_time()
        if self.age >= self.LIFESPAN:
            self.remove(*self.groups())
            Snag(self.visibleGroup, self.obstaclesGroup, self.rect.midbottom, self.loadedImages, self.clock)

    def getSaveData(self) -> list:
        return [self.rect.midbottom, self.currentDurability, self.age]