import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups, obstacleSprites, entityData):
        super().__init__(groups)

        self.imageUp    = pygame.image.load(entityData["path_to_image_up"]).convert_alpha()
        self.imageDown  = pygame.image.load(entityData["path_to_image_down"]).convert_alpha()
        self.imageLeft  = pygame.image.load(entityData["path_to_image_left"]).convert_alpha()
        self.imageRight = pygame.image.load(entityData["path_to_image_right"]).convert_alpha()
        self.image = self.imageDown
        self.rect = self.image.get_rect(center = entityData["position_center"])

        self.speed = entityData["speed"]
        self.direction = pygame.math.Vector2()
        self.obstacleSprites = obstacleSprites

    def collision(self, direction): # Only for non moving coliders!
        if direction == "horizontal":
            for sprite in self.obstacleSprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0: # moving East
                        self.rect.right = sprite.rect.left
                    else: # moving West
                        self.rect.left = sprite.rect.right

        if direction == "vertical":
            for sprite in self.obstacleSprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y < 0: # moving North
                        self.rect.top = sprite.rect.bottom
                    else: # moving South
                        self.rect.bottom = sprite.rect.top

    def move(self):
        if self.direction.x != 0 and self.direction.y != 0:
            self.direction = self.direction.normalize()
            # self.direction = self.direction * 0.707 slightly more efficient but this approach assumes that entity can move ony 8 directions ([1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]) and is not properly handling anything in between like ([1,0.5])

        self.rect.x += round(self.direction.x * self.speed)
        self.collision("horizontal")

        self.rect.y += round(self.direction.y * self.speed)
        self.collision("vertical")

        self.changeImage()
        self.direction.xy = [0, 0]

    def changeImage(self):
        if self.direction.x > 0:
            self.image = self.imageRight
        elif self.direction.x < 0:
            self.image = self.imageLeft

        if self.direction.y > 0:
            self.image = self.imageDown
        elif self.direction.y < 0:
            self.image = self.imageUp
