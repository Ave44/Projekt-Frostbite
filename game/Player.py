import pygame

from game.Entity import Entity
from game.ui.SelectedItem import SelectedItem
from game.ui.Ui import Ui


class Player(Entity):
    def __init__(self, groups, obstacleSprites, playerData):
        super().__init__(groups, obstacleSprites, playerData)
        self._selectedItem = SelectedItem(playerData['position_center'])
        self.ui = Ui(groups[0], self._selectedItem, playerData['position_center'])

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
        self.ui.update(self.rect.center)
        self._selectedItem.playerPos = self.rect.center
