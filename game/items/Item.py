import pygame
import shortuuid

from config import ROOT_PATH


class Item(pygame.sprite.Sprite):
    def __init__(self, spriteGroup: pygame.sprite.Group, center: pygame.math.Vector2()):
        super().__init__([spriteGroup])
        self.spriteGroup = spriteGroup
        self.id = shortuuid.uuid()
        self.name = "Item without name"
        self.image = pygame.image.load(f"{ROOT_PATH}/graphics/items/undefined.png")
        self.icon = pygame.image.load(f"{ROOT_PATH}/graphics/items/undefined.png")
        self.rect = self.image.get_rect(center = center)


    def drop(self, position: pygame.math.Vector2()) -> None:
        self.rect.center = position
        self.addToSpriteGroup()

    def addToSpriteGroup(self):
        self.add(self.spriteGroup)

    def removeFromSpriteGroup(self):
        self.remove(self.spriteGroup)