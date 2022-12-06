import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, spriteGroups, obstacleSprites, entityData: dict):
        super().__init__(spriteGroups)

        self.imageUp = pygame.image.load(entityData["path_to_image_up"]).convert_alpha()
        self.imageDown = pygame.image.load(entityData["path_to_image_down"]).convert_alpha()
        self.imageLeft = pygame.image.load(entityData["path_to_image_left"]).convert_alpha()
        self.imageRight = pygame.image.load(entityData["path_to_image_right"]).convert_alpha()
        self.image = self.imageDown
        self.rect = self.image.get_rect(center=entityData["position_center"])

        self.speed = entityData["speed"]
        self.direction = pygame.math.Vector2()
        self.obstacleSprites = obstacleSprites

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

    def move(self):
        if self.direction.x != 0 and self.direction.y != 0:
            self.direction = self.direction.normalize()

        self.rect.x += round(self.direction.x * self.speed)
        self.checkHorizontalCollision()

        self.rect.y += round(self.direction.y * self.speed)
        self.checkVerticalCollision()

        self.adjustImageToDirection()
        self.direction.xy = [0, 0]

    def adjustImageToDirection(self):
        if self.direction.x > 0:
            self.image = self.imageRight
        elif self.direction.x < 0:
            self.image = self.imageLeft

        if self.direction.y > 0:
            self.image = self.imageDown
        elif self.direction.y < 0:
            self.image = self.imageUp
