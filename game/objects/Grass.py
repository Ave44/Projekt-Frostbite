from pygame.math import Vector2
from pygame.time import Clock
from pygame.sprite import Group
from game.LoadedImages import LoadedImages

from game.objects.domain.Object import Object
from game.objects.domain.AnimatedObject import AnimatedObject
from game.items.GrassFibers import GrassFibers
from game.items.domain.Shovel import Shovel
from game.entities.Player import Player


class Grass(Object, AnimatedObject):
    def __init__(self, visibleSprites: Group, midbottom: Vector2, loadedImages: LoadedImages,
                 clock: Clock, currGrowthTime: int = None, currentDurability: int = None):
        self.loadedImages = loadedImages
        image = loadedImages.grass[0]
        Object.__init__(self, visibleSprites, midbottom, 1, Shovel, image, currentDurability)
        AnimatedObject.__init__(self, loadedImages.grass, clock, 120)

        self.imagePicked = loadedImages.grassPicked
        self.regrowthTimeMs = 10000
        self.currGrowthTime = currGrowthTime if currGrowthTime else 0

        if currGrowthTime:
            self.currGrowthTime = currGrowthTime
            self.picked = True
            self.image = self.imagePicked
        else:
            self.currGrowthTime = 0
            self.picked = False

    def onLeftClickAction(self, player: Player) -> None:
        if not self.picked:
            self.picked = True
            self.currGrowthTime = 0
            self.image = self.imagePicked
            grass = GrassFibers(self.visibleSprites, self.rect.midbottom, self.loadedImages)
            player.inventory.addItem(grass, player.selectedItem)

    def drop(self) -> None:
        GrassFibers(self.visibleSprites, self.rect.midbottom, self.loadedImages)

    def grow(self):
        self.currGrowthTime += self.clock.get_time()
        if self.currGrowthTime >= self.regrowthTimeMs:
            self.picked = False

    def update(self) -> None:
        if self.picked:
            self.grow()
        else:
            AnimatedObject.animationUpdate(self)

    def getSaveData(self) -> dict:
        return {'midbottom': self.rect.midbottom, 'currentDurability': self.currentDurability, 'currGrowthTime': self.currGrowthTime}

    def setSaveData(self, savefileData: dict):
        self.rect.midbottom = savefileData['midbottom']
        self.currentDurability = savefileData['currentDurability']
        self.currGrowthTime = savefileData['currGrowthTime']
