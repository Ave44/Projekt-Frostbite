from pygame import Vector2
from pygame.image import load
from pygame.sprite import Sprite


class Entity(Sprite):
    def __init__(self, spriteGroups, obstacleSprites, entityData: dict):
        super().__init__(spriteGroups)

        self.imageUp = load(entityData["path_to_image_up"]).convert_alpha()
        self.imageDown = load(entityData["path_to_image_down"]).convert_alpha()
        self.imageLeft = load(entityData["path_to_image_left"]).convert_alpha()
        self.imageRight = load(entityData["path_to_image_right"]).convert_alpha()
        self.image = self.imageDown
        self.rect = self.image.get_rect(center=entityData["position_center"])

        self.speed = entityData["speed"]
        self.direction = Vector2()
        self.obstacleSprites = obstacleSprites

        self.maxHealth = entityData["maxHealth"]
        self.currentHealth = entityData["currentHealth"]

        self.destinationPosition = None
        self.destinationTarget = None

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
            self.currentHealth = 0
            self.die()
        else:
            self.currentHealth -= amount

    def die(self):
        self.currentHealth = 0
        self.remove(*self.groups())

    def heal(self, amount: int):
        if self.currentHealth + amount >= self.maxHealth:
            self.currentHealth = self.maxHealth
        else:
            self.currentHealth += amount
