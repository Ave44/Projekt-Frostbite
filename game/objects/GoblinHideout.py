from pygame import Vector2
from pygame.time import Clock
from game.LoadedImages import LoadedImages
from game.LoadedSounds import LoadedSounds

from game.entities.Goblin import Goblin
from game.items.domain.Hammer import Hammer
from game.objects.domain.Object import Object
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites

from game.items.GoblinFang import GoblinFang


class GoblinHideout(Object):
    def __init__(self, visibleGroup: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: LoadedImages, loadedSounds: LoadedSounds, midBottom: Vector2,
                 clock: Clock, daysFromGoblinsChange: int = None):
        image = loadedImages.goblinHideout
        Object.__init__(self, visibleGroup, midBottom, 50, Hammer, image)
        self.loadedImages = loadedImages
        self.loadedSounds = loadedSounds
        self.goblins = []
        self.daysFromGoblinsChange = daysFromGoblinsChange if daysFromGoblinsChange else 0
        self.numberOfGoblinsToSpawn = 2
        self.obstacleSprites = obstacleSprites
        self.clock = clock

        self.spawnGoblins()

    def spawnGoblins(self):
        pos = Vector2(self.rect.centerx, self.rect.centery)
        for i in range(0, self.numberOfGoblinsToSpawn):
            newGoblin = Goblin(self.visibleGroup, self.obstacleSprites, self.loadedImages, self.loadedSounds, self.clock, pos)
            self.goblins.append(newGoblin)
        self.daysFromGoblinsChange = 0

    def interact(self) -> None:
        print("interacted with goblin hideout")

    def drop(self) -> None:
        GoblinFang(self.visibleSprites, self.rect.center, self.loadedImages)
        GoblinFang(self.visibleSprites, self.rect.center, self.loadedImages)
        GoblinFang(self.visibleSprites, self.rect.center, self.loadedImages)

    def onNewDay(self):
        if len(self.goblins) >= 2:
            return

        if self.daysFromGoblinsChange < 2:
            self.daysFromGoblinsChange += 1
            return

        self.spawnGoblins()

    def getSaveData(self) -> list:
        return [self.rect.midbottom, self.currentDurability, self.daysFromGoblinsChange]