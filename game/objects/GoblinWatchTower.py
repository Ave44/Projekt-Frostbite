from math import sqrt

from pygame import Vector2
from pygame.time import Clock

from game.LoadedImages import LoadedImages
from game.LoadedSounds import LoadedSounds
from game.entities.GoblinChampion import GoblinChampion
from game.entities.Player import Player
from game.SoundPlayer import SoundPlayer

from game.entities.Goblin import Goblin
from game.entities.domain.State import State
from game.items.domain.Axe import Axe
from game.objects.domain.Object import Object
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites

from game.items.GoblinFang import GoblinFang


class GoblinWatchTower(Object):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: LoadedImages, loadedSounds: LoadedSounds, midbottom: Vector2, clock: Clock,
                 soundPlayer: SoundPlayer, destroyTower: callable,
                 daysUntilPotentialActivation: int = 0, goblinDataList: list[dict] = None,
                 goblinChampionDataList: list[dict] = None
                 ):
        image = loadedImages.goblinWatchTower
        Object.__init__(self, visibleSprites, midbottom, 15, Axe, image)
        self.loadedImages = loadedImages
        self.loadedSounds = loadedSounds
        self.numberOfGoblinsToSpawn = 3
        self.obstacleSprites = obstacleSprites
        self.clock = clock
        self.daysUntilPotentialActivation = daysUntilPotentialActivation
        self.visibleSprites = visibleSprites
        self.goblins: list[Goblin] = []
        self.goblinChampion: list[GoblinChampion] = []
        self.soundPlayer = soundPlayer
        self.destroyTower = destroyTower
        self.goblinsInside = True

        if goblinDataList is not None:
            for goblinData in goblinDataList:
                goblin = self.spawnGoblin(goblinData['midbottom'], goblinData['currHealth'])
                goblin.remove(visibleSprites)
        else:
            for i in range(self.numberOfGoblinsToSpawn):
                goblin = self.spawnGoblin(self.rect.midbottom)
                goblin.remove(visibleSprites)

        if goblinChampionDataList is not None:
            for goblinChampionData in goblinChampionDataList:
                goblinChampion = self.spawnGoblinChampion(goblinChampionData['midbottom'],
                                                          goblinChampionData['currHealth'])
                goblinChampion.remove(visibleSprites)
        else:
            goblinChampion = self.spawnGoblinChampion(self.rect.midbottom)
            goblinChampion.remove(visibleSprites)

    def spawnAggressiveGoblins(self, player: Player) -> None:
        self.goblinsInside = False
        pos = Vector2(self.rect.centerx, self.rect.centery)
        if len(self.goblins) != 0:
            self.revealAggressiveGoblins(player, pos)
            return
        if self.daysUntilPotentialActivation == 0:
            for i in range(0, self.numberOfGoblinsToSpawn):
                goblin = Goblin(self.visibleSprites, self.obstacleSprites, self.loadedImages, self.loadedSounds,
                                self.clock, pos, self.soundPlayer)
                goblin.moveToOrAttack(player)
                self.goblins.append(goblin)
            goblinChampion = GoblinChampion(self.visibleSprites, self.obstacleSprites, self.loadedImages,
                                            self.loadedSounds, self.clock, pos, self.soundPlayer)
            goblinChampion.moveToOrAttack(player)
            self.goblins.append(goblinChampion)
            self.daysUntilPotentialActivation = 1

    def goblinChampionStateCheck(self) -> None:
        if len(self.goblinChampion) != 0:
            goblinChampion = self.goblinChampion[0]
            if goblinChampion.state == State.DEAD:
                self.goblinChampion.pop(0)
            else:
                goblinChampion.currHealth = goblinChampion.maxHealth
                goblinChampion.add(goblinChampion.visibleSprites)

    def goblinListStateCheck(self) -> None:
        for goblin in self.goblins:
            if goblin.state == State.DEAD:
                indexToRemove = self.goblins.index(goblin)
                self.goblins.pop(indexToRemove)
            else:
                goblin.currHealth = goblin.maxHealth
                goblin.add(goblin.visibleSprites)

    def revealAggressiveGoblins(self, player: Player, pos: Vector2) -> None:
        self.goblinListStateCheck()
        self.goblinChampionStateCheck()
        if len(self.goblins) != 3 and self.daysUntilPotentialActivation:
            for i in range(0, 3 - len(self.goblins)):
                goblin = self.spawnGoblin(pos)
                goblin.moveToOrAttack(player)
                self.daysUntilPotentialActivation = 1
        if len(self.goblinChampion) != 1 and self.daysUntilPotentialActivation:
            goblin = self.spawnGoblinChampion(pos)
            goblin.moveToOrAttack(player)
            self.daysUntilPotentialActivation = 1

    def drop(self) -> None:
        GoblinFang(self.visibleSprites, self.rect.center, self.loadedImages)

    def onNewDay(self) -> None:
        if self.daysUntilPotentialActivation != 0:
            self.daysUntilPotentialActivation -= 1

    def checkForPlayer(self) -> Player | None:
        for entity in self.visibleSprites.entities:
            if isinstance(entity, Player):
                distance = sqrt((self.rect.centerx - entity.rect.centerx) ** 2 +
                                (self.rect.bottom - entity.rect.bottom) ** 2)
                if distance < 300:
                    return entity
        return None

    def update(self) -> None:
        player = self.checkForPlayer()
        if player:
            if self.goblinsInside:
                self.spawnAggressiveGoblins(player)
        elif not self.goblinsInside:
            allGoblinsAtHome = True
            for goblin in [*self.goblins, *self.goblinChampion]:
                goblin.setDestination(Vector2(self.rect.midbottom), None)
                if goblin.rect.midbottom == self.rect.midbottom:
                    goblin.remove(goblin.visibleSprites)
                else:
                    allGoblinsAtHome = False
            if allGoblinsAtHome:
                self.goblinsInside = True

    def destroy(self) -> None:
        self.destroyTower()
        self.kill()
        self.drop()
        for goblin in [*self.goblins, *self.goblinChampion]:
            goblin.isHomeless = True

    def spawnGoblin(self, pos, currentHealth: int = None) -> Goblin:
        goblin = Goblin(self.visibleSprites, self.obstacleSprites, self.loadedImages, self.loadedSounds,
                        self.clock, pos, self.soundPlayer, currentHealth)
        self.goblins.append(goblin)
        return goblin

    def spawnGoblinChampion(self, pos, currentHealth: int = None) -> GoblinChampion:
        goblinChampion = GoblinChampion(self.visibleSprites, self.obstacleSprites, self.loadedImages,
                                        self.loadedSounds, self.clock, pos, self.soundPlayer, currentHealth)
        self.goblinChampion.append(goblinChampion)
        return goblinChampion

    def getSaveData(self) -> dict:
        goblinDataList = []
        goblinChampionDataList = []
        for goblin in self.goblins:
            goblinDataList.append(goblin.getSaveData(True))
        for goblin in self.goblinChampion:
            goblinChampionDataList.append(goblin.getSaveData(True))
        return {
            'midbottom': self.rect.midbottom,
            'currentDurability': self.currentDurability,
            'daysUntilPotentialActivation': self.daysUntilPotentialActivation,
            'goblinDataList': goblinDataList,
            'goblinChampionDataList': goblinChampionDataList
        }
