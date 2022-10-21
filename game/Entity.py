import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.direction = pygame.math.Vector2()
        self.speed = 1

    def move(self):
        if self.direction.x != 0 and self.direction.y != 0:
            self.direction = self.direction * 0.707
        self.rect.center += pygame.math.Vector2(round(self.direction.x * self.speed), round(self.direction.y * self.speed))
        self.direction.xy = [0, 0]
