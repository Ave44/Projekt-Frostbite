import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("./graphics/tiles/grass.png")
        self.rect = self.image.get_rect(topleft=position)
