from math import sqrt

from pygame import Vector2
from pygame.time import Clock

from game.LoadedImages import LoadedImages
from game.LoadedSounds import LoadedSounds
from game.entities.GoblinChampion import GoblinChampion
from game.entities.Player import Player

from game.entities.Goblin import Goblin
from game.entities.domain.State import State
from game.items.domain.Axe import Axe
from game.objects.domain.Object import Object
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites

from game.items.GoblinFang import GoblinFang


class GoblinWatchTower(Object):
    def __init__(self, visibleGroup: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: LoadedImages, loadedSounds: LoadedSounds, midBottom: Vector2, clock: Clock):
        image = loadedImages.goblinWatchTower
        Object.__init__(self, visibleGroup, midBottom, 50, Axe, image)
        self.loadedImages = loadedImages
        self.loadedSounds = loadedSounds
        self.numberOfGoblinsToSpawn = 4
        self.obstacleSprites = obstacleSprites
        self.clock = clock
        self.daysUntilPotentialActivation = 0
        self.visibleSprites = visibleGroup
        self.goblins: list[Goblin] = []

    def spawnAggressiveGoblins(self, player: Player) -> None:
        pos = Vector2(self.rect.centerx, self.rect.centery)
        if len(self.goblins) != 0:
            self.revealAggressiveGoblins(player, pos)
            return
        if self.daysUntilPotentialActivation == 0:
            for i in range(0, self.numberOfGoblinsToSpawn):
                goblin = Goblin(self.visibleSprites, self.obstacleSprites, self.loadedImages, self.loadedSounds,
                                self.clock, pos)
                goblin.attack(player)
                self.goblins.append(goblin)
            goblinChampion = GoblinChampion(self.visibleSprites, self.obstacleSprites, self.loadedImages,
                                            self.loadedSounds, self.clock, pos)
            goblinChampion.attack(player)
            self.goblins.append(goblinChampion)
            self.daysUntilPotentialActivation = 1
        return

    def revealAggressiveGoblins(self, player: Player, pos: Vector2) -> None:
        for goblin in self.goblins:
            if goblin.state == State.DEAD:
                indexToRemove = self.goblins.index(goblin)
                self.goblins.pop(indexToRemove)
            else:
                goblin.add(goblin.visibleSprites)
        if len(self.goblins) != 4 and self.daysUntilPotentialActivation:
            for i in range(0, 4 - len(self.goblins)):
                goblin = Goblin(self.visibleSprites, self.obstacleSprites, self.loadedImages, self.loadedSounds,
                                self.clock, pos)
                goblin.attack(player)
                self.goblins.append(goblin)
                self.daysUntilPotentialActivation = 1
        return

    def interact(self) -> None:
        print("interacted with goblin watch tower")

    def drop(self) -> None:
        GoblinFang(self.visibleSprites, self.rect.center, self.loadedImages)

    def onNewDay(self) -> None:
        if self.daysUntilPotentialActivation != 0:
            self.daysUntilPotentialActivation -= 1
        return

    def checkForPlayer(self) -> Player | None:
        for entity in self.visibleSprites.entities:
            if isinstance(entity, Player):
                distance = sqrt((self.rect.centerx - entity.rect.centerx) ** 2 +
                                (self.rect.bottom - entity.rect.bottom) ** 2)
                if distance < 300:
                    return entity
        return None

    def update(self) -> None:
        if self.checkForPlayer():
            player = self.checkForPlayer()
            self.spawnAggressiveGoblins(player)
        if not self.checkForPlayer():
            for goblin in self.goblins:
                goblin.remove(*goblin.groups())

    def destroy(self) -> None:
        self.remove(*self.groups())
        self.kill()
        self.drop()
