import pygame
from game.Entity import Entity

class Player(Entity):
    def __init__(self, position, groups, obstacleSprites):
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/player/player_down.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        self.obstacleSprites = obstacleSprites

        self.direction = pygame.math.Vector2()
        self.speed = 5


    def input(self):
        pressedKeys = pygame.key.get_pressed()

        # vertical directions
        if pressedKeys[pygame.K_w]:
            self.direction.y = -1
        elif pressedKeys[pygame.K_s]:
            self.direction.y = 1

        # horizontal directions
        if pressedKeys[pygame.K_a]:
            self.direction.x = -1
        elif pressedKeys[pygame.K_d]:
            self.direction.x = 1
            

    def update(self):
        self.input()
        self.move()