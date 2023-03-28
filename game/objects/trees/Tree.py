from game.objects.domain.CollisionObject import CollisionObject
from game.objects.domain.Flammable import Flammable

from game.items.domain.Item import Item
from game.objects.trees.BurntTree import BurntTree

from pygame import Vector2, Rect
from pygame.time import Clock
from pygame.sprite import Group
from game.items.domain.ToolType import ToolType

class Tree(CollisionObject, Flammable):
    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, midBottom: Vector2,
                 loadedImages: list, clock: Clock, growthStage: int, ageMs: int = 0):
        self.loadedImages = loadedImages
        image = loadedImages.tree[0]

        colliderRect = Rect((0, 0), (5, 5))
        colliderRect.midbottom = midBottom
        CollisionObject.__init__(self, visibleGroup, obstaclesGroup, midBottom, 5,
                                 ToolType.AXE, image, colliderRect)
        Flammable.__init__(self, clock)

        self.growthStage = growthStage
        self.age = ageMs
        self.lifespans = []

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
        if self.age >= self.lifespans[self.growthStage]:
            self.growthStage += 1
            MediumTree(self.visibleGroup, self.obstaclesGroup, self.rect.midbottom, self.loadedImages, self.clock)
