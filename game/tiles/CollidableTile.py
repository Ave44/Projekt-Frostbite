import pygame
from pygame.sprite import AbstractGroup


class CollidableTile(pygame.sprite.Sprite):
    def __init__(self, position,image, groups: AbstractGroup):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
