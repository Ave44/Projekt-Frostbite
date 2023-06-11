from pygame import Vector2
from pygame.time import Clock
from game.LoadedImages import LoadedImages
from game.LoadedSounds import LoadedSounds
from game.SoundPlayer import SoundPlayer
from game.dayCycle.DayCycle import DayCycle
from game.dayCycle.domain.DayPhase import DayPhase
from game.dayCycle.domain.DayPhaseListener import DayPhaseListener

from game.entities.Goblin import Goblin

from game.items.domain.Hammer import Hammer
from game.objects.domain.Object import Object
from game.objects.factories.GoblinFactory import GoblinFactory
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites

from game.items.GoblinFang import GoblinFang


class GoblinHideout(Object, DayPhaseListener):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: LoadedImages, loadedSounds: LoadedSounds, midbottom: Vector2,
                 clock: Clock, soundPlayer: SoundPlayer, dayCycle: DayCycle,
                 daysFromGoblinsChange: int = None, currentDurability: int = None,
                 goblinsDataList: list[dict] = None):
        image = loadedImages.goblinHideout
        Object.__init__(self, visibleSprites, midbottom, 50, Hammer, image, currentDurability)
        self.loadedImages = loadedImages
        self.loadedSounds = loadedSounds
        self.dayCycle = dayCycle

        self.goblins: list[Goblin] = []
        self.daysFromGoblinsChange = daysFromGoblinsChange if daysFromGoblinsChange else 0
        self.obstacleSprites = obstacleSprites
        self.clock = clock
        self.soundPlayer = soundPlayer
        self.goblinFactory = GoblinFactory(self.visibleSprites, self.obstacleSprites, self.loadedImages,
                                           self.loadedSounds, self.clock, self.soundPlayer)

        self.dayCycle.events.subscribe(DayPhase.DAY, self)

        if goblinsDataList is not None:
            for goblinData in goblinsDataList:
                self.goblinFactory.createGoblin(goblinData['midbottom'], goblinData['currHealth'])
        else:
            self.spawnGoblin()
            self.spawnGoblin()

    def spawnGoblin(self):
        pos = Vector2(self.rect.centerx, self.rect.bottom)
        newGoblin = self.goblinFactory.createGoblin(pos)
        self.goblins.append(newGoblin)
        self.daysFromGoblinsChange = 0

    def interact(self) -> None:
        print("interacted with goblin hideout")

    def drop(self) -> None:
        GoblinFang(self.visibleSprites, self.rect.midbottom, self.loadedImages)
        GoblinFang(self.visibleSprites, self.rect.midbottom, self.loadedImages)
        GoblinFang(self.visibleSprites, self.rect.midbottom, self.loadedImages)
        self.dayCycle.events.unsubscribe(DayPhase.DAY)

    def onDay(self):
        if len(self.goblins) >= 2:
            return

        if self.daysFromGoblinsChange < 2:
            self.daysFromGoblinsChange += 1
            return

        self.spawnGoblin()

    def destroy(self) -> None:
        Object.destroy()
        for goblin in self.goblins:
            goblin.isHomeless = True

    def getSaveData(self) -> dict:
        goblinsDataList = []
        for goblin in self.goblins:
            goblinsDataList.append(goblin.getSaveData(True))
        return {'midbottom': self.rect.midbottom, 'currentDurability': self.currentDurability, 'daysFromGoblinsChange': self.daysFromGoblinsChange, 'goblinsDataList': goblinsDataList}
    
    def setSaveData(self, savefileData: dict):
        self.rect.midbottom = savefileData['midbottom']
        self.currentDurability = savefileData['currentDurability']
        self.daysFromGoblinsChange = savefileData['daysFromGoblinsChange']
        for goblinData in savefileData['daysFromGoblinsChange']:
            self.goblinFactory.createGoblin(goblinData['midbottom'], goblinData['currHealth'])
