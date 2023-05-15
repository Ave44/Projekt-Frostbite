from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
    from game.spriteGroups.ObstacleSprites import ObstacleSprites
    from game.entities.effects.Effect import Effect

from abc import abstractmethod, ABC
from math import sqrt, ceil

from pygame import Vector2, Surface, Rect
from pygame.sprite import Sprite
from pygame.time import Clock

from game.entities.domain.State import State
from game.objects.domain.CollisionObject import CollisionObject


class Entity(Sprite, ABC):
    def __init__(self, spriteGroup: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 entityData: dict, entityImages: dict[Surface], entitySounds: dict,
                 colliderRect: Rect, clock: Clock, midbottom: Vector2, currHealth: int = None):

        Sprite.__init__(self, spriteGroup)
        spriteGroup.entities.add(self)
        savefileGroup = getattr(spriteGroup.savefileGroups, type(self).__name__)
        savefileGroup.add(self)

        self.soundIdle = entitySounds["idle"]
        self.soundMovement = entitySounds["movement"]
        self.soundAttack = entitySounds["attack"]
        self.soundDamaged = entitySounds["damaged"]

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
        self.colliderRect = colliderRect
        self.colliderRect.midbottom = self.rect.midbottom

        self.speed = entityData["speed"]
        self.direction = Vector2()
        self.obstacleSprites = obstacleSprites
        self.actionRange = entityData["actionRange"]

        self.maxHealth = entityData["maxHealth"]
        if currHealth:
            self.currHealth = currHealth
        else:
            self.currHealth = self.maxHealth
        self.timeFromLastHealthChange = 0
        self._state = State.NORMAL

        self.destinationPosition = None
        self.midDestinationPosition = None
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

    def findClosestOtherEntity(self) -> Entity | None:
        closestEntity = None
        closestDistance = float('inf')
        for entity in self.visibleSprites.entities:
            if isinstance(self, type(entity)) or isinstance(entity, type(self)):
                continue
            distance = sqrt((self.rect.centerx - entity.rect.centerx) ** 2 +
                            (self.rect.bottom - entity.rect.bottom) ** 2)
            if distance < closestDistance:
                closestEntity = entity
                closestDistance = distance
        return closestEntity

    def checkHorizontalCollision(self):
        for sprite in self.obstacleSprites.getObstacles(self.colliderRect.center):
            if not sprite.colliderRect.colliderect(self.colliderRect):
                pass
            elif self.direction.x > 0:
                self.colliderRect.right = sprite.colliderRect.left
            else:
                self.colliderRect.left = sprite.colliderRect.right

    def checkVerticalCollision(self):
        for sprite in self.obstacleSprites.getObstacles(self.colliderRect.center):
            if not sprite.colliderRect.colliderect(self.colliderRect):
                pass
            elif self.direction.y < 0:
                self.colliderRect.top = sprite.colliderRect.bottom
            else:
                self.colliderRect.bottom = sprite.colliderRect.top

    def checkForCollision(self, oldRect: Rect, newRect: Rect) -> tuple[bool, dict]:
        collisions = {'horizontal': None, 'vertical': None}
        isCollision = False
        horizontalChange = Rect(newRect.x, oldRect.y, oldRect.width, oldRect.height)
        verticalChange = Rect(oldRect.x, newRect.y, oldRect.width, oldRect.height)

        for sprite in self.obstacleSprites.getObstacles(newRect.center):
            if sprite.colliderRect.colliderect(newRect):
                isCollision = True
                if sprite.colliderRect.colliderect(horizontalChange):
                    collisions['horizontal'] = sprite.colliderRect
                elif sprite.colliderRect.colliderect(verticalChange):
                    collisions['vertical'] = sprite.colliderRect
                else:
                    collisions['horizontal'] = sprite.colliderRect
                    collisions['vertical'] = sprite.colliderRect
        return isCollision, collisions

    def handleCollision(self, verticallyColidingRect: Rect | None, horizontallyColidingRect: Rect | None):
        self.midDestinationPosition = Vector2(self.colliderRect.centerx, self.colliderRect.bottom)
        if horizontallyColidingRect:
            topDistanceToDestination = abs(horizontallyColidingRect.top - self.destinationPosition.y)
            bottomDistanceToDestination = abs(horizontallyColidingRect.bottom - self.destinationPosition.y)
            if topDistanceToDestination <= bottomDistanceToDestination:
                self.midDestinationPosition.y = horizontallyColidingRect.top
            else:
                self.midDestinationPosition.y = horizontallyColidingRect.bottom + self.colliderRect.height
        if verticallyColidingRect:
            leftDistanceToDestination = abs(verticallyColidingRect.left - self.destinationPosition.x)
            rightDistanceToDestination = abs(verticallyColidingRect.right - self.destinationPosition.x)
            if leftDistanceToDestination <= rightDistanceToDestination:
                self.midDestinationPosition.x = verticallyColidingRect.left - ceil(self.colliderRect.width / 2)
            else:
                self.midDestinationPosition.x = verticallyColidingRect.right + ceil(self.colliderRect.width / 2)

    def setDestination(self, position: Vector2, target: Sprite | None = None):
        self.destinationTarget = target
        self.destinationPosition = position
        self.midDestinationPosition = None
        self.direction = Vector2(0, 0)

    def isInRange(self, target: Vector2, rangeDistance: int) -> bool:
        distance = sqrt((self.colliderRect.centerx - target.x) ** 2 +
                        (self.colliderRect.bottom - target.y) ** 2)
        return distance <= rangeDistance

    def checkIfRachedDestination(self) -> bool:
        if self.destinationTarget:
            if isinstance(self.destinationTarget, CollisionObject):
                return self.checkIfReachedCollisionObject(self.destinationTarget)
            return self.checkIfReachedNonCollisionTarget()
        return self.checkIfReachedDestinationPosition()

    def checkIfReachedCollisionObject(self, collisionObject: CollisionObject) -> bool:
        if (abs(self.colliderRect.left - collisionObject.colliderRect.right) > self.actionRange
                and abs(self.colliderRect.right - collisionObject.colliderRect.left) > self.actionRange):
            return False
        if (abs(self.colliderRect.top - collisionObject.colliderRect.bottom) > self.actionRange
                and abs(self.colliderRect.bottom - collisionObject.colliderRect.top) > self.actionRange):
            return False

        self.direction = Vector2(self.destinationTarget.colliderRect.centerx - self.colliderRect.centerx, self.destinationTarget.colliderRect.bottom - self.colliderRect.bottom)
        self.adjustImageToDirection()
        collisionObject.onLeftClickAction(self)
        self.setDestination(None)
        return True

    def checkIfReachedNonCollisionTarget(self):
        if not self.isInRange(self.destinationPosition, self.actionRange):
            return False
        self.direction = Vector2(self.destinationTarget.rect.centerx - self.colliderRect.centerx, self.destinationTarget.rect.bottom - self.colliderRect.bottom)
        self.adjustImageToDirection()
        self.destinationTarget.onLeftClickAction(self)
        self.setDestination(None)
        return True

    def checkIfReachedDestinationPosition(self):
        if self.colliderRect.midbottom == self.destinationPosition:
            self.setDestination(None)
            return True
        return False

    def moveToPosition(self, position: Vector2):
        xOffset = position.x - self.colliderRect.centerx
        yOffset = position.y - self.colliderRect.bottom
        if abs(xOffset) <= self.speed and abs(yOffset) <= self.speed:
            self.direction = Vector2(xOffset, yOffset)
            self.adjustImageToDirection()
            self.colliderRect.midbottom = position
            self.direction = Vector2(0, 0)
        else:
            newDirection = Vector2(xOffset, yOffset)
            newDirection = newDirection.normalize()

            self.direction.xy = newDirection
            self.adjustImageToDirection()

        newRect = Rect(self.colliderRect.x + round(self.direction.x * self.speed),
                       self.colliderRect.y + round(self.direction.y * self.speed),
                       self.colliderRect.width, self.colliderRect.height)

        isCollision, colidingSprites = self.checkForCollision(self.colliderRect, newRect)
        if isCollision:
            self.handleCollision(colidingSprites['vertical'], colidingSprites['horizontal'])
        else:
            self.colliderRect.midbottom = newRect.midbottom

    def move(self):
        if self.destinationPosition:
            if self.midDestinationPosition:
                self.moveToPosition(self.midDestinationPosition)
                if self.colliderRect.midbottom == self.midDestinationPosition:
                    self.midDestinationPosition = None
            elif not self.checkIfRachedDestination():
                self.moveToPosition(self.destinationPosition)
            self.adjustRect()

        elif self.direction != Vector2(0, 0):
            self.moveInDirection()

    def moveInDirection(self):
        self.direction = self.direction.normalize()

        self.colliderRect.x += round(self.direction.x * self.speed)
        self.checkHorizontalCollision()

        self.colliderRect.y += round(self.direction.y * self.speed)
        self.checkVerticalCollision()

        self.adjustImageToDirection()
        self.adjustRect()

    def adjustImageToDirection(self):
        if abs(self.direction.x) > abs(self.direction.y):
            if self.direction.x > 0:
                self.image = self.imageRight
            else:
                self.image = self.imageLeft
        else:
            if self.direction.y > 0:
                self.image = self.imageDown
            else:
                self.image = self.imageUp

    def adjustRect(self):
        self.rect.midbottom = self.colliderRect.midbottom

    def getDamage(self, amount: int, damageCause: str = None) -> None:
        if self.state != State.DEAD:
            if self.currHealth <= amount:
                if damageCause:
                    self.die(damageCause)
                else:
                    self.die()
            else:
                self.timeFromLastHealthChange = 0
                self.state = State.DAMAGED
                self.currHealth -= amount

    def die(self):
        self.state = State.DEAD
        self.currHealth = 0
        self.remove(*self.groups())
        self.drop()

    def onLeftClickAction(self, player):
        self.getDamage(player.damage())

    def heal(self, amount: int):
        if self.currHealth != self.maxHealth:
            self.timeFromLastHealthChange = 0
            self.state = State.HEALED
        if self.currHealth + amount >= self.maxHealth:
            self.currHealth = self.maxHealth
        else:
            self.currHealth += amount

    def addEffect(self, effect: Effect) -> None:
        filteredActiveEffects = list(filter(lambda x: (x.__class__ != effect.__class__), self.activeEffects))
        filteredActiveEffects.append(effect)
        self.activeEffects = filteredActiveEffects

    def playSound(self, sound):
        sound.play()

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

    def getSaveData(self) -> dict:
        return {'midbottom': self.rect.midbottom, 'currHealth': self.currHealth}
    
    def setSaveData(self, savefileData: dict) -> None:
        self.rect.midbottom = savefileData['midbottom']
        self.currHealth = savefileData['currHealth']
