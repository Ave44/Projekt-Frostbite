from math import sqrt

from pygame import Vector2
from pygame.time import Clock

from game.LoadedImages import LoadedImages
from game.LoadedSounds import LoadedSounds
from game.entities.Player import Player

from game.entities.Goblin import Goblin
from game.items.domain.Hammer import Hammer
from game.objects.domain.Object import Object
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites

from game.items.GoblinFang import GoblinFang


class GoblinWarningHorn(Object):
    def __init__(self, visibleGroup: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: LoadedImages, loadedSounds: LoadedSounds, midBottom: Vector2, clock: Clock):
        image = loadedImages.goblinHorn
        Object.__init__(self, visibleGroup, midBottom, 50, Hammer, image)
        self.loadedImages = loadedImages
        self.loadedSounds = loadedSounds
        self.numberOfGoblinsToSpawn = 6
        self.obstacleSprites = obstacleSprites
        self.clock = clock
        self.daysUntilPotentialActivation = 0
        self.visibleSprites = visibleGroup

    def spawnAggressiveGoblins(self, player: Player):
        pos = Vector2(self.rect.centerx, self.rect.centery)
        for i in range(0, self.numberOfGoblinsToSpawn):
            goblin = Goblin(self.visibleSprites, self.obstacleSprites, self.loadedImages, self.loadedSounds, self.clock, pos)
            goblin.attack(player)
        self.daysUntilPotentialActivation = 5

    def interact(self) -> None:
        print("interacted with goblin horn")

    def drop(self) -> None:
        GoblinFang(self.visibleSprites, self.rect.center, self.loadedImages)

    def onNewDay(self) -> None:
        if self.daysUntilPotentialActivation != 0:
            self.daysUntilPotentialActivation -= 1
        return

    def canSpawnGoblins(self):
        if self.daysUntilPotentialActivation == 0:
            return True
        return False

    def checkForPlayer(self) -> Player | None:
        if self.canSpawnGoblins():
            for entity in self.visibleSprites.entities:
                if isinstance(entity, Player):
                    distance = sqrt((self.rect.centerx - entity.rect.centerx) ** 2 +
                                    (self.rect.bottom - entity.rect.bottom) ** 2)
                    if distance < 300:
                        return entity
        return None

    def update(self) -> None:
        if self.canSpawnGoblins():
            if self.checkForPlayer():
                player = self.checkForPlayer()
                self.spawnAggressiveGoblins(player)
