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
    def __init__(self, visibleSprites: Group, obstacleSprites: Group, midbottom: Vector2,
                 loadedImages: LoadedImages, clock: Clock, ageMs: int = 0, currentDurability: int = None):
        self.loadedImages = loadedImages
        image = loadedImages.largeTree[0]
        colliderRect = Rect((0, 0), (20, 20))
        colliderRect.midbottom = midbottom

        CollisionObject.__init__(self, visibleSprites, obstacleSprites,
                                 midbottom, 10, Axe, image, colliderRect, currentDurability)
        Flammable.__init__(self, clock)

        self.ageMs = ageMs
        self.growthStage = 3
        self.LIFESPAN = 20000

    def interact(self) -> None:
        print("interacted with medium trees")  # in the future there will be a real implementation

    def drop(self) -> None:
        Wood(self.visibleSprites, self.rect.center, self.loadedImages)
        Wood(self.visibleSprites, self.rect.center, self.loadedImages)
        Wood(self.visibleSprites, self.rect.center, self.loadedImages)
        Accorn(self.visibleSprites, self.rect.center, self.loadedImages)

    def burn(self):
        self.remove(*self.groups())
        BurntTree(self.visibleSprites, self.obstacleSprites, self.rect.midbottom, self.loadedImages)

    def update(self):
        if self.isOnFire and self.timeToBurn:
            self.flameUpdate()
            return
        self.ageMs += self.clock.get_time()
        if self.ageMs >= self.LIFESPAN:
            self.remove(*self.groups())
            Snag(self.visibleSprites, self.obstacleSprites, self.rect.midbottom, self.loadedImages, self.clock)

    def getSaveData(self) -> dict:
        return {'midbottom': self.rect.midbottom, 'currentDurability': self.currentDurability, 'ageMs': self.ageMs}
    
    def setSaveData(self, savefileData: dict):
        self.rect.midbottom = savefileData['midbottom']
        self.currentDurability = savefileData['currentDurability']
        self.ageMs = savefileData['ageMs']
