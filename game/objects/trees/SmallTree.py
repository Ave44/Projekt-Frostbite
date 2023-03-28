from pygame import Vector2, Rect
from pygame.sprite import Group
from pygame.time import Clock

from game.items.domain.Item import Item
from game.items.domain.ToolType import ToolType
from game.objects.domain.CollisionObject import CollisionObject
from game.objects.domain.Flammable import Flammable
from game.objects.trees.BurntTree import BurntTree
from game.objects.trees.MediumTree import MediumTree


class SmallTree(CollisionObject, Flammable):
    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, midBottom: Vector2,
                 loadedImages: list, clock: Clock, ageMs: int = 0):
        self.loadedImages = loadedImages
        image = loadedImages.smallTree[0]
        colliderRect = Rect((0, 0), (5, 5))
        colliderRect.midbottom = midBottom

        CollisionObject.__init__(self, visibleGroup, obstaclesGroup, midBottom, 5,
                                 ToolType.AXE, image, colliderRect)
        Flammable.__init__(self, clock)

        self.age = ageMs
        self.growthStage = 1
        self.LIFESPAN = 20000

    def interact(self) -> None:
        print("interacted with small trees")  # in the future there will be a real implementation

    def drop(self) -> None:
        Item(self.visibleGroup, self.rect.center)  # in the future there will be a real implementation

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
            MediumTree(self.visibleGroup, self.obstaclesGroup, self.rect.midbottom, self.loadedImages, self.clock)
