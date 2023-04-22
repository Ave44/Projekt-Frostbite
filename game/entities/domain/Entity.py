from abc import abstractmethod, ABC
from math import sqrt

from pygame import Vector2, Surface, Rect
from pygame.sprite import Sprite
from pygame.time import Clock

from game.entities.domain.State import State


class Entity(Sprite, ABC):
    from game.entities.effects.Effect import Effect

    def __init__(self, spriteGroup, obstacleSprites, entityData: dict, entityImages: dict[Surface], clock: Clock, midbottom: Vector2, currHealth: int = None):
        from game.entities.effects.Effect import Effect

        Sprite.__init__(self, spriteGroup)
        spriteGroup.entities.add(self)

        self.imageUpNormal = entityImages["image_up"]
        self.imageDownNormal = entityImages["image_down"]
        self.imageLeftNormal = entityImages["image_left"]
        self.imageRightNormal = entityImages["image_right"]

        self.imageUpHeal = entityImages["image_up_heal"]
        self.imageDownHeal = entityImages["image_down_heal"]
        self.imageLeftHeal = entityImages["image_left_heal"]
        self.imageRightHeal = entityImages["image_right_heal"]

        self.imageUpDamage = entityImages["image_up_damage"]
        self.imageDownDamage = entityImages["image_down_damage"]
        self.imageLeftDamage = entityImages["image_left_damage"]
        self.imageRightDamage = entityImages["image_right_damage"]

        self.imageUp = self.imageUpNormal
        self.imageDown = self.imageDownNormal
        self.imageLeft = self.imageLeftNormal
        self.imageRight = self.imageRightNormal

        self.image: Surface = self.imageDown
        self.rect: Rect = self.image.get_rect(midbottom=midbottom)

        self.speed = entityData["speed"]
        self.direction = Vector2()
        self.obstacleSprites = obstacleSprites
        self.actionRange = entityData["actionRange"]

        self.maxHealth = entityData["maxHealth"]
        if currHealth:
            self.currentHealth = currHealth
        else:
            self.currentHealth = self.maxHealth
        self.timeFromLastHealthChange = 0
        self._state = State.NORMAL

        self.destinationPosition = None
        self.destinationTarget = None

        self.activeEffects: list[Effect] = []
        self.clock = clock

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, newState: State) -> None:
        if newState == State.DAMAGED:
            self.__changeImages(self.imageUpDamage, self.imageDownDamage, self.imageLeftDamage, self.imageRightDamage)
        elif newState == State.HEALED:
            self.__changeImages(self.imageUpHeal, self.imageDownHeal, self.imageLeftHeal, self.imageRightHeal)
        else:
            self.__changeImages(self.imageUpNormal, self.imageDownNormal, self.imageLeftNormal, self.imageRightNormal)
        self._state = newState

    def __changeImages(self, newImageUp: Surface, newImageDown: Surface, newImageLeft: Surface, newImageRight: Surface):
        if self.image == self.imageUp:
            self.image = newImageUp
        elif self.image == self.imageDown:
            self.image = newImageDown
        elif self.image == self.imageLeft:
            self.image = newImageLeft
        else:
            self.image = newImageRight

        self.imageUp = newImageUp
        self.imageDown = newImageDown
        self.imageLeft = newImageLeft
        self.imageRight = newImageRight

    @abstractmethod
    def localUpdate(self):
        pass

    @abstractmethod
    def drop(self) -> None:
        pass

    def checkHorizontalCollision(self):  # Solution only for non-moving coliders!
        for sprite in self.obstacleSprites.getObstacles(self.rect.center):
            if not sprite.colliderRect.colliderect(self.rect):
                pass
            elif self.direction.x > 0:
                self.rect.right = sprite.colliderRect.left
            else:
                self.rect.left = sprite.colliderRect.right

    def checkVerticalCollision(self):
        for sprite in self.obstacleSprites.getObstacles(self.rect.center):
            if not sprite.colliderRect.colliderect(self.rect):
                pass
            elif self.direction.y < 0:
                self.rect.top = sprite.colliderRect.bottom
            else:
                self.rect.bottom = sprite.colliderRect.top

    def setDestination(self, position: Vector2, target: Sprite):
        self.destinationTarget = target
        self.destinationPosition = position

    def adjustDirection(self):
        if self.destinationPosition:
            self.moveTowards()

    def isInRange(self, target: Vector2, rangeDistance: int) -> bool:
        distance = sqrt((self.rect.centerx - target.x) ** 2 +
                        (self.rect.bottom - target.y) ** 2)
        return distance <= rangeDistance

    def moveTowards(self):
        if self.isInRange(self.destinationPosition, self.actionRange):
            self.destinationPosition = None
            if self.destinationTarget:
                self.destinationTarget.onLeftClickAction(self)
                self.destinationTarget = None
        else:
            xOffset = self.destinationPosition.x - self.rect.centerx
            yOffset = self.destinationPosition.y - self.rect.bottom
            if abs(xOffset) <= self.speed and abs(yOffset) <= self.speed:
                self.rect.midbottom = self.destinationPosition
                self.direction = Vector2(0, 0)
            else:
                newDirection = Vector2(xOffset, yOffset)
                self.direction.xy = newDirection

    def move(self):
        if self.direction.x != 0 or self.direction.y != 0:
            self.direction = self.direction.normalize()

        self.rect.x += round(self.direction.x * self.speed)
        self.checkHorizontalCollision()

        self.rect.y += round(self.direction.y * self.speed)
        self.checkVerticalCollision()

        self.adjustImageToDirection()
        self.adjustDirection()

    def adjustImageToDirection(self):
        if self.direction.x > 0:
            self.image = self.imageRight
        elif self.direction.x < 0:
            self.image = self.imageLeft

        if self.direction.y > 0:
            self.image = self.imageDown
        elif self.direction.y < 0:
            self.image = self.imageUp

    def getDamage(self, amount: int) -> None:
        if self.currentHealth <= amount:
            self.die()
        if self.state != State.DEAD:
            self.timeFromLastHealthChange = 0
            self.state = State.DAMAGED
            self.currentHealth -= amount

    def die(self):
        self.state = State.DEAD
        self.currentHealth = 0
        self.remove(*self.groups())
        self.drop()

    def heal(self, amount: int):
        if self.currentHealth != self.maxHealth:
            self.timeFromLastHealthChange = 0
            self.state = State.HEALED
        if self.currentHealth + amount >= self.maxHealth:
            self.currentHealth = self.maxHealth
        else:
            self.currentHealth += amount

    def addEffect(self, effect: Effect) -> None:
        filteredActiveEffects = list(filter(lambda x: (x.__class__ != effect.__class__), self.activeEffects))
        filteredActiveEffects.append(effect)
        self.activeEffects = filteredActiveEffects

    def update(self) -> None:
        self.localUpdate()

        timeFromLastTick = self.clock.get_time()
        for effect in self.activeEffects:
            effect.execute()

        if self.state != State.NORMAL:
            if self.timeFromLastHealthChange >= 250:
                self.state = State.NORMAL
            else:
                self.timeFromLastHealthChange += timeFromLastTick
