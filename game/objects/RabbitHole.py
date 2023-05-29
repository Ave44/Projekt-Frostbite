from pygame import Vector2
from pygame.time import Clock

from game.dayCycle.DayCycle import DayCycle
from game.dayCycle.domain.DayPhase import DayPhase
from game.dayCycle.domain.DayPhaseListener import DayPhaseListener
from game.entities.Rabbit import Rabbit
from game.items.domain.Shovel import Shovel
from game.objects.domain.Object import Object
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites
from game.LoadedSounds import LoadedSounds
from game.LoadedImages import LoadedImages


class RabbitHole(Object, DayPhaseListener):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites, dayCycle: DayCycle,
                 loadedImages: LoadedImages, loadedSounds: LoadedSounds, midbottom: Vector2,
                 clock: Clock, daysFromRabbitsChange: int = 0, currentDurability: int = None,
                 rabbitsDataList: list[dict] = None):
        image = loadedImages.rabbitHole
        Object.__init__(self, visibleSprites, midbottom, 2, Shovel, image, currentDurability)
        self.loadedImages = loadedImages
        self.loadedSounds = loadedSounds
        self.dayCycle = dayCycle

        self.rabbits: list[Rabbit] = []
        self.daysFromRabbitsChange = daysFromRabbitsChange
        self.obstacleSprites = obstacleSprites
        self.clock = clock

        self.dayCycle.events.subscribe(DayPhase.DAY, self)
        self.dayCycle.events.subscribe(DayPhase.EVENING, self)

        if rabbitsDataList is not None:
            for rabbitData in rabbitsDataList:
                self.spawnRabbit(rabbitData)
        else:
            for i in range(3):
                self.spawnRabbit()

    def spawnRabbit(self, rabbitData: dict = None):
        pos = Vector2(self.rect.centerx, self.rect.centery)
        if rabbitData:
            newRabbit = Rabbit(self.visibleSprites, self.obstacleSprites, self.loadedImages, self.loadedSounds,
                               self.clock, rabbitData['midbottom'], self, rabbitData['currHealth'])
        else:
            newRabbit = Rabbit(self.visibleSprites, self.obstacleSprites, self.loadedImages, self.loadedSounds,
                               self.clock, pos, self)
        self.rabbits.append(newRabbit)
        self.daysFromRabbitsChange = 0

    def releaseRabbits(self):
        for rabbit in self.rabbits:
            if rabbit.isInHome:
                rabbit.goOut()

    def hideRabbits(self):
        for rabbit in self.rabbits:
            if not rabbit.isInHome:
                rabbit.runHome()

    def drop(self) -> None:
        for rabbit in self.rabbits:
            rabbit.isHomeless = True
            rabbit.goOut()
        self.dayCycle.events.unsubscribe(DayPhase.DAY)
        self.dayCycle.events.unsubscribe(DayPhase.EVENING)

    def interact(self) -> None:
        print("interacted with rabbit hole")

    def onDay(self):
        self.releaseRabbits()

        if len(self.rabbits) >= 3:
            return

        if self.daysFromRabbitsChange < 10:
            self.daysFromRabbitsChange += 1
            return

        self.spawnRabbit()

    def onEvening(self):
        self.hideRabbits()

    def getSaveData(self) -> dict:
        rabbitsDataList = []
        for rabbit in self.rabbits:
            rabbitsDataList.append(rabbit.getSaveData(True))
        return {'midbottom': self.rect.midbottom, 'currentDurability': self.currentDurability,
                'daysFromRabbitsChange': self.daysFromRabbitsChange, 'rabbitsDataList': rabbitsDataList}

    def setSaveData(self, savefileData: dict):
        self.rect.midbottom = savefileData['midbottom']
        self.currentDurability = savefileData['currentDurability']
        self.daysFromRabbitsChange = savefileData['daysFromRabbitsChange']
        for rabbitData in savefileData['rabbitsDataList']:
            self.spawnRabbit(rabbitData)
