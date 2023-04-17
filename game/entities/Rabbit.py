from pygame import Vector2
from pygame.time import Clock
from game.LoadedImages import LoadedImages

from game.entities.domain.PassiveMob import PassiveMob
from game.items.SmallMeat import SmallMeat
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites

class Rabbit(PassiveMob):

    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: LoadedImages, clock: Clock, midbottom: Vector2, home = None, currHealth: int = None):
        entityData = {
            "speed": 2,
            "maxHealth": 5
        }
        PassiveMob.__init__(self, visibleSprites, obstacleSprites, loadedImages.rabbit, clock, entityData, 200, 2000, 500, 1500, midbottom, currHealth)
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
        # if self.home:
            # self.home.rabbits.remove(self)
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
