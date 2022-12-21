import pygame
import shortuuid
from pygame.math import Vector2

from config import ROOT_PATH


class Item(pygame.sprite.Sprite):
    def __init__(self, sprite_group: pygame.sprite.Group, center: Vector2()):
        super().__init__(sprite_group)
        self.spriteGroup = sprite_group
        self.id = shortuuid.uuid()
        self.name = "Item without name"
        self.image = pygame.image.load(f"{ROOT_PATH}/graphics/items/undefined.png")
        self.icon = pygame.image.load(f"{ROOT_PATH}/graphics/items/undefined.png")
        self.rect = self.image.get_rect(center=center)

    def drop(self, position: Vector2()) -> None:
        self.rect.center = position
        self.addToSpriteGroup()

    def action(self, entity):
        entity.inventory.addItem(self, entity.selectedItem)

    def addToSpriteGroup(self):
        self.add(self.spriteGroup)

    def removeFromSpriteGroup(self):
        self.remove(self.spriteGroup)
