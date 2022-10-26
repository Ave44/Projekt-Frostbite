import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, index, groups):
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/tiles/sea.png")
        self.rect = self.image.get_rect(topleft = position)

        if index == 1:
            self.image = pygame.image.load("./graphics/tiles/grass.png")
