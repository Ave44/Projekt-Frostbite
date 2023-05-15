from game.entities.domain.Entity import Entity
from abc import ABC

from pygame import Vector2, Surface, Rect
from pygame.sprite import Sprite
from pygame.time import Clock

from game.entities.domain.State import State


class AnimatedEntity(ABC):
    def __init__(self, spriteGroup, entityImages: dict[Surface], clock: Clock):
        Sprite.__init__(self, spriteGroup)
        spriteGroup.entities.add(self)

        self.timeOnFrame = 0
        self.timeMsBetweenFrames = 100
        self.currentImageFrame = 0

        self.imageIdleNormal = entityImages["images_idle"]
        self.imageUpNormal = entityImages["images_up"]
        self.imageDownNormal = entityImages["images_down"]
        self.imageLeftNormal = entityImages["images_left"]
        self.imageRightNormal = entityImages["images_right"]

        self.imageIdleHeal = entityImages["images_idle_heal"]
        self.imageUpHeal = entityImages["images_up_heal"]
        self.imageDownHeal = entityImages["images_down_heal"]
        self.imageLeftHeal = entityImages["images_left_heal"]
        self.imageRightHeal = entityImages["images_right_heal"]

        self.imageIdleDamage = entityImages["images_idle_damage"]
        self.imageUpDamage = entityImages["images_up_damage"]
        self.imageDownDamage = entityImages["images_down_damage"]
        self.imageLeftDamage = entityImages["images_left_damage"]
        self.imageRightDamage = entityImages["images_right_damage"]

        self.imageIdle = self.imageIdleNormal
        self.imageUp = self.imageUpNormal
        self.imageDown = self.imageDownNormal
        self.imageLeft = self.imageLeftNormal
        self.imageRight = self.imageRightNormal

        self.image: Surface = self.imageIdle[0]

        self.clock = clock

    def state(self, newState: State) -> None:
        if newState == State.DAMAGED:
            self.__changeImages(self.imageIdleDamage[self.currentImageFrame % len(self.imageIdleDamage)],
                                self.imageUpDamage[self.currentImageFrame % len(self.imageUpDamage)],
                                self.imageDownDamage[self.currentImageFrame % len(self.imageDownDamage)],
                                self.imageLeftDamage[self.currentImageFrame % len(self.imageLeftDamage)],
                                self.imageRightDamage[self.currentImageFrame % len(self.imageRightDamage)])
        elif newState == State.HEALED:
            self.__changeImages(self.imageIdleHeal[self.currentImageFrame % len(self.imageIdleHeal)],
                                self.imageUpHeal[self.currentImageFrame % len(self.imageUpHeal)],
                                self.imageDownHeal[self.currentImageFrame % len(self.imageDownHeal)],
                                self.imageLeftHeal[self.currentImageFrame % len(self.imageLeftHeal)],
                                self.imageRightHeal[self.currentImageFrame % len(self.imageRightHeal)])
        else:
            self.__changeImages(self.imageIdleNormal[self.currentImageFrame % len(self.imageIdleNormal)],
                                self.imageUpNormal[self.currentImageFrame % len(self.imageUpNormal)],
                                self.imageDownNormal[self.currentImageFrame % len(self.imageDownNormal)],
                                self.imageLeftNormal[self.currentImageFrame % len(self.imageLeftNormal)],
                                self.imageRightNormal[self.currentImageFrame % len(self.imageRightNormal)])
        self._state = newState

    def __changeImages(self, newImageIdle: Surface, newImageUp: Surface, newImageDown: Surface, newImageLeft: Surface, newImageRight: Surface):
        if self.image in self.imageIdle:
            self.image = newImageIdle
        elif self.image in self.imageUp:
            self.image = newImageUp
        elif self.image in self.imageDown:
            self.image = newImageDown
        elif self.image in self.imageLeft:
            self.image = newImageLeft
        elif self.image in self.imageRight:
            self.image = newImageRight
        else:
            pass
        self.imageIdle = newImageRight
        self.imageUp = newImageUp
        self.imageDown = newImageDown
        self.imageLeft = newImageLeft
        self.imageRight = newImageRight

    def adjustImageToDirection(self):

        if abs(self.direction.x) > abs(self.direction.y):
            if self.direction.x > 0:
                self.image = self.imageRight[self.currentImageFrame % len(self.imageRight)]
            else:
                self.image = self.imageLeft[self.currentImageFrame % len(self.imageLeft)]
        else:
            if self.direction.y > 0:
                self.image = self.imageDown[self.currentImageFrame % len(self.imageDown)]
            else:
                self.image = self.imageUp[self.currentImageFrame % len(self.imageUp)]
        if self.direction.x == 0 and self.direction.y == 0:
            self.image = self.imageIdle[self.currentImageFrame % len(self.imageIdle)]

    def update(self) -> None:
        self.localUpdate()
        self.timeOnFrame += self.clock.get_time()
        if self.timeOnFrame >= self.timeMsBetweenFrames:
            self.timeOnFrame = 0
            self.currentImageFrame += 1
