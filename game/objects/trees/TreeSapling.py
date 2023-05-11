from pygame import Vector2, Rect
from pygame.sprite import Group
from pygame.time import Clock
from game.LoadedImages import LoadedImages

from game.items.domain.Item import Item
from game.items.domain.Shovel import Shovel
from game.objects.domain.CollisionObject import CollisionObject
from game.objects.trees.SmallTree import SmallTree


class TreeSapling(CollisionObject):
    _LIFESPAN = 20000

    def __init__(self, visibleGroup: Group, obstaclesGroup: Group, midBottom: Vector2,
                 loadedImages: LoadedImages, clock: Clock):
        self.loadedImages = loadedImages
        image = loadedImages.treeSapling[0]
        colliderRect = Rect((0, 0), (5, 5))
        colliderRect.midbottom = midBottom
        CollisionObject.__init__(self, visibleGroup, obstaclesGroup,
                                 midBottom, 1, Shovel, image, colliderRect)

        self.clock = clock
        self.age = 0
        self.growthStage = 0

    def interact(self) -> None:
        print("interacted with sapling")  # in the future there will be a real implementation

    def drop(self) -> None:
        Item(self.visibleGroup, self.rect.center)

    def update(self) -> None:
        self.age += self.clock.get_time()
        if self.age >= self._LIFESPAN:
            self.remove(*self.groups())
            SmallTree(self.visibleGroup, self.obstaclesGroup, self.rect.midbottom, self.loadedImages, self.clock)

    def getSaveData(self) -> list:
        return [self.rect.midbottom, self.currentDurability, self.age]