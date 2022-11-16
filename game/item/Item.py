import pygame
import shortuuid

from config import ROOT_PATH


class Item(pygame.sprite.Sprite):
    def __init__(self, groups: list[pygame.sprite.Group], center: pygame.math.Vector2()):
        super().__init__(groups)
        self.id = shortuuid.uuid()
        self.name = "Item without name"
        self.image = pygame.image.load(f"{ROOT_PATH}/graphics/items/undefined.png")
        self.icon = pygame.image.load(f"{ROOT_PATH}/graphics/items/undefined.png")
        self.rect = self.image.get_rect(center = center)


    def drop(self, pos: pygame.math.Vector2()) -> None:
        self.rect.center = pos
