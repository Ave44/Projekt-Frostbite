import pygame
from pygame.sprite import AbstractGroup


class SeaTile(pygame.sprite.Sprite):
    def __init__(self, position, groups: AbstractGroup):
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/tiles/sea.png")
        self.rect = self.image.get_rect(topleft=position)
