from pygame import Vector2, Rect
from pygame.sprite import Group
from pygame.time import Clock
from game.LoadedImages import LoadedImages

from game.items.domain.Item import Item
from game.items.domain.Axe import Axe
from game.objects.domain.CollisionObject import CollisionObject
from game.objects.domain.Flammable import Flammable
from game.objects.trees.BurntTree import BurntTree


class Snag(CollisionObject, Flammable):

    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, midBottom: Vector2, 
                 loadedImages: LoadedImages, clock: Clock, age: int = 0):
        self.loadedImages = loadedImages
        image = loadedImages.snag[0]
        colliderRect = Rect((0, 0), (5, 5))
        colliderRect.midbottom = midBottom

        CollisionObject.__init__(self, visibleGroup, obstaclesGroup,
                                 midBottom, 1, Axe, image, colliderRect)
        Flammable.__init__(self, clock)

        self.age = age
        self.growthStage = 4
        self.LIFESPAN = 10000

    def interact(self) -> None:
        print("interacted with snag")  # in the future there will be a real implementation

    def drop(self) -> None:
        Item(self.visibleGroup, self.rect.center)  # in the future there will be a real implementation

    def burn(self):
        self.remove(*self.groups())
        BurntTree(self.visibleGroup, self.obstaclesGroup, self.rect.midbottom, self.loadedImages)

    def update(self):
        from game.objects.trees.SmallTree import SmallTree

        if self.isOnFire and self.timeToBurn:
            self.flameUpdate()
            return
        self.age += self.clock.get_time()
        if self.age >= self.LIFESPAN:
            self.remove(*self.groups())
            SmallTree(self.visibleGroup, self.obstaclesGroup, self.rect.midbottom, self.loadedImages, self.clock)
