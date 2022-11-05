from abc import ABC

import pygame.sprite
import shortuuid

class Item(pygame.sprite.Sprite, ABC):
    def __init__(self, name: str, pathToImage: str, pathToIcon: str):
        super().__init__()
        self._id = shortuuid.uuid()
        self._name = name

        self.image = pygame.image.load(pathToImage)
        self.icon = pygame.image.load(pathToIcon)
        self.rect = self.image.get_rect()

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    def drop(self, pos: tuple[int, int]) -> None:
        self.remove()
        self.rect.center = pos

    def use(self):
        pass
