from abc import abstractmethod, ABC

from pygame import Vector2
from pygame.image import load
from pygame.sprite import Sprite
from pygame.time import Clock

from game.entities.State import State


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
            self.imageUp = self.imageUpDamage
            self.imageDown = self.imageDownDamage
            self.imageLeft = self.imageLeftDamage
            self.imageRight = self.imageRightDamage
        elif newState == State.HEALED:
            self.imageUp = self.imageUpHeal
            self.imageDown = self.imageDownHeal
            self.imageLeft = self.imageLeftHeal
            self.imageRight = self.imageRightHeal
        else:
            self.imageUp = self.imageUpNormal
            self.imageDown = self.imageDownNormal
            self.imageLeft = self.imageLeftNormal
            self.imageRight = self.imageRightNormal

    @abstractmethod
    def localUpdate(self):
        pass

    def checkHorizontalCollision(self):  # Solution only for non-moving coliders!
        for sprite in self.obstacleSprites:
            if not sprite.rect.colliderect(self.rect):
                pass
            elif self.direction.x > 0:
                self.rect.right = sprite.rect.left
            else:
                self.rect.left = sprite.rect.right

    def checkVerticalCollision(self):
        for sprite in self.obstacleSprites:
            if not sprite.rect.colliderect(self.rect):
                pass
            elif self.direction.y < 0:
                self.rect.top = sprite.rect.bottom
            else:
                self.rect.bottom = sprite.rect.top

    def setDestination(self, position: Vector2, target: Sprite):
        self.destinationTarget = target
        self.destinationPosition = position

    def adjustDirection(self):
        if self.destinationPosition:
            self.moveTowards()
        else:
            self.direction.xy = [0, 0]

    def moveTowards(self):
        if Vector2(self.rect.midbottom) == self.destinationPosition:
            self.destinationPosition = None
            if self.destinationTarget:
                self.destinationTarget.action(self)
                self.destinationTarget = None
        else:
            xOffset = self.destinationPosition.x - self.rect.centerx
            yOffset = self.destinationPosition.y - self.rect.bottom
            if abs(xOffset) <= self.speed and abs(yOffset) <= self.speed:
                self.rect.midbottom = self.destinationPosition
                self.direction = Vector2(0, 0)
            else:
                newDirection = Vector2(xOffset, yOffset).normalize()
                self.direction.xy = newDirection

    def move(self):
        if self.direction.x != 0 and self.direction.y != 0:
            self.direction = self.direction.normalize()

        self.rect.x += round(self.direction.x * self.speed)
        self.checkHorizontalCollision()

        self.rect.y += round(self.direction.y * self.speed)
        self.checkVerticalCollision()

        self.adjustDirection()
        self.adjustImageToDirection()

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
        else:
            self.currentHealth -= amount
            self.timeFromLastHealthChange = 0
            self.state = State.DAMAGED

    def die(self):
        self.currentHealth = 0
        self.remove(*self.groups())

    def heal(self, amount: int):
        if self.currentHealth + amount >= self.maxHealth:
            self.currentHealth = self.maxHealth
        else:
            self.currentHealth += amount
            self.timeFromLastHealthChange = 0
            self.state = State.HEALED

    def addEffect(self, effect: Effect) -> None:
        filteredActiveEffects = list(filter(lambda x: (x.__class__ != effect.__class__), self.activeEffects))
        filteredActiveEffects.append(effect)
        self.activeEffects = filteredActiveEffects

    def executeEffect(self, effect: Effect) -> None:
        if not effect.amountOfTicks:
            self.activeEffects.remove(effect)
        else:
            effect.execute()

    def update(self) -> None:
        self.localUpdate()

        timeFromLastTick = self.clock.get_time()
        for effect in self.activeEffects:
            self.executeEffect(effect)

        if not self.state == State.NORMAL:
            return
        if self.timeFromLastHealthChange >= 250:
            self.state = State.NORMAL
        else:
            self.timeFromLastHealthChange += timeFromLastTick
