import pygame

from game.item.Item import Item


class SelectedItem(pygame.sprite.Sprite):
    def __init__(self, playerPos: pygame.math.Vector2(), item: Item = None):
        super().__init__()
        self.playerPos = playerPos
        self.item = item
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()

    def isEmpty(self) -> bool:
        return True if self.item is None else False

    def removeItem(self) -> None:
        self.item = None

    def drop(self) -> None:
        self.item.drop(self.playerPos)

    def updatePos(self, newPos: pygame.math.Vector2()) -> None:
        self.rect.center = newPos
