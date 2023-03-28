from abc import abstractmethod, ABC

from pygame import Vector2, Surface

from pygame.image import load
from pygame.sprite import Sprite
from pygame.time import Clock

from game.entities.domain.State import State


class Entity(Sprite, ABC):
    from game.entities.effects.Effect import Effect

    def __init__(self, spriteGroup, obstacleSprites, entityData: dict, clock: Clock):
        from game.entities.effects.Effect import Effect

        super().__init__(spriteGroup)
        spriteGroup.entities.add(self)

        self.imageUpNormal = load(entityData["path_to_image_up"]).convert_alpha()
        self.imageDownNormal = load(entityData["path_to_image_down"]).convert_alpha()
        self.imageLeftNormal = load(entityData["path_to_image_left"]).convert_alpha()
        self.imageRightNormal = load(entityData["path_to_image_right"]).convert_alpha()

        self.imageUpHeal = load(entityData["path_to_image_up_heal"]).convert_alpha()
        self.imageDownHeal = load(entityData["path_to_image_down_heal"]).convert_alpha()
        self.imageLeftHeal = load(entityData["path_to_image_left_heal"]).convert_alpha()
        self.imageRightHeal = load(entityData["path_to_image_right_heal"]).convert_alpha()

        self.imageUpDamage = load(entityData["path_to_image_up_damage"]).convert_alpha()
        self.imageDownDamage = load(entityData["path_to_image_down_damage"]).convert_alpha()
        self.imageLeftDamage = load(entityData["path_to_image_left_damage"]).convert_alpha()
        self.imageRightDamage = load(entityData["path_to_image_right_damage"]).convert_alpha()

        self.imageUp = self.imageUpNormal
        self.imageDown = self.imageDownNormal
        self.imageLeft = self.imageLeftNormal
        self.imageRight = self.imageRightNormal

        self.image = self.imageDown
        self.rect = self.image.get_rect(center=entityData["position_center"])

        self.speed = entityData["speed"]
        self.direction = Vector2()
        self.obstacleSprites = obstacleSprites

        self.maxHealth = entityData["maxHealth"]
        self.currentHealth = entityData["currentHealth"]
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

    def moveTowards(self):
        if Vector2(self.rect.midbottom) == self.destinationPosition:
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
        if self.currentHealth:
            self.timeFromLastHealthChange = 0
            self.state = State.DAMAGED
        if self.currentHealth <= amount:
            self.die()
        else:
            self.currentHealth -= amount

    def die(self):
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