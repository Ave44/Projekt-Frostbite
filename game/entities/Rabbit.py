from pygame import Vector2, Rect
from pygame.time import Clock

from game.entities.domain.PassiveMob import PassiveMob
from game.items.SmallMeat import SmallMeat
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites
from game.LoadedSounds import LoadedSounds
from game.LoadedImages import LoadedImages


class Rabbit(PassiveMob):

    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: LoadedImages, loadedSounds: LoadedSounds, clock: Clock, midbottom: Vector2, home=None, currHealth: int = None):
        entityData = {
            "speed": 2,
            "maxHealth": 5,
            "actionRange": 10,
            "sightRange": 200,
            "moveEveryMs": 2000,
            "minMoveTimeMs": 500,
            "maxMoveTimeMs": 1500
        }
        colliderRect = Rect((0, 0), (10, 10))
        PassiveMob.__init__(self, visibleSprites, obstacleSprites, loadedImages.rabbit, loadedSounds.rabbit, colliderRect, clock, entityData, midbottom, currHealth)
        self.loadedImages = loadedImages
        self.home = home
        self.isRunningHome = False
        self.isInHome = False
        self.isHomeless = False
        if not home:
            self.isHomeless = True
            self.homePosition = None
        else:
            self.homePosition = Vector2(self.home.rect.centerx, self.home.rect.centery)

    def drop(self) -> None:
        SmallMeat(self.visibleSprites, self.rect.center, self.loadedImages)

    def runHome(self):
        self.setDestination(self.homePosition, None)
        self.isRunningHome = True

    def hide(self):
        self.isRunningHome = False
        self.isInHome = True
        self.remove(*self.groups())

    def goOut(self):
        self.add(self.visibleSprites)
        self.isInHome = False

    def getDamage(self, amount: int) -> None:
        self.runHome()
        super().getDamage(amount)

    def die(self):
        if self.home:
            if self in self.home.rabbits:
                self.home.rabbits.remove(self)
        super().die()

    def localUpdate(self):
        if self.isHomeless:
            super().localUpdate()
        elif self.rect.midbottom == self.homePosition and self.isRunningHome:
            self.hide()
        elif self.destinationPosition:
            self.move()
        else:
            super().localUpdate()

    def getSaveData(self, homeRequest: bool = False) -> dict:
        if self.isHomeless or homeRequest:
            return {'midbottom': self.rect.midbottom, 'currHealth': self.currHealth, 'home': None}
