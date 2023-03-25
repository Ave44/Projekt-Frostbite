import pygame
import shortuuid
from pygame import Surface
from pygame.math import Vector2

from config import ROOT_PATH
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class Item(pygame.sprite.Sprite):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2,  name: str = None,
                 image: Surface = None, icon: Surface = None):
        super().__init__(visibleSprites)
        self.visibleSprites = visibleSprites
        self.id = shortuuid.uuid()

        self.name = name
        if not name:
            self.name = "Unknown"

        self.image = image
        if not image:
            self.image = pygame.image.load(f"{ROOT_PATH}/graphics/items/undefined.png")

        self.icon = icon
        if not icon:
            self.icon = pygame.image.load(f"{ROOT_PATH}/graphics/items/undefined.png")

        self.rect = self.image.get_rect(center=center)

    def drop(self, position: Vector2) -> None:
        self.rect.center = position
        self.show()

    def pickUp(self, player):
        player.inventory.addItem(self, player.selectedItem)

    def show(self):
        self.add(self.visibleSprites)

    def hide(self):
        self.remove(self.visibleSprites)
