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

    def __init__(self, visibleSprites: Group, obstacleSprites: Group, midbottom: Vector2,
                 loadedImages: LoadedImages, clock: Clock, ageMs: int = 0):
        self.loadedImages = loadedImages
        image = loadedImages.treeSapling[0]
        colliderRect = Rect((0, 0), (5, 5))
        colliderRect.midbottom = midbottom
        CollisionObject.__init__(self, visibleSprites, obstacleSprites,
                                 midbottom, 1, Shovel, image, colliderRect)

        self.clock = clock
        self.ageMs = ageMs
        self.growthStage = 0

    def interact(self) -> None:
        print("interacted with sapling")  # in the future there will be a real implementation

    def drop(self) -> None:
        pass

    def update(self) -> None:
        self.ageMs += self.clock.get_time()
        if self.ageMs >= self._LIFESPAN:
            self.remove(*self.groups())
            SmallTree(self.visibleSprites, self.obstacleSprites, self.rect.midbottom, self.loadedImages, self.clock)

    def getSaveData(self) -> dict:
        return {'midbottom': self.rect.midbottom, 'currentDurability': self.currentDurability, 'ageMs': self.ageMs}
    
    def setSaveData(self, savefileData: dict):
        self.rect.midbottom = savefileData['midbottom']
        self.currentDurability = savefileData['currentDurability']
        self.ageMs = savefileData['ageMs']
