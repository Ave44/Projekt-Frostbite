import pygame

from game.Entity import Entity
from game.Inventory import Inventory


class Player(Entity):
    def __init__(self, groups, obstacleSprites, playerData):
        super().__init__(groups, obstacleSprites, playerData)
        self._selectedItem = None
        self.inventory = Inventory(groups[0], 5, 10, self.rect.center, self._selectedItem)

    def input(self):
        pressedKeys = pygame.key.get_pressed()

        # vertical directions
        if pressedKeys[pygame.K_w]:
            self.direction.y = -1
        elif pressedKeys[pygame.K_s]:
            self.direction.y = 1

        # horizontal directions
        if pressedKeys[pygame.K_a]:
            self.direction.x = -1
        elif pressedKeys[pygame.K_d]:
            self.direction.x = 1

    def update(self):
        self.input()
        self.move()
        if self.inventory.isOpened:
            self.inventory.playerPos = self.rect.center
