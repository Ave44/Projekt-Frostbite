import pygame

from game.Entity import Entity
from game.ui.SelectedItem import SelectedItem
from game.ui.Ui import Ui
from game.ui.inventory.Inventory import Inventory


class Player(Entity):
    def __init__(self, 
                groups: list[pygame.sprite.Group],
                obstacleSprites: pygame.sprite.Group,
                playerData,
                inventory: Inventory,
                selectedItem: SelectedItem):

        super().__init__(groups, obstacleSprites, playerData)
        self.selectedItem = selectedItem
        self.inventory = inventory


    def moveUp(self):
        self.direction.y = -1

    def moveDown(self):
        self.direction.y = 1

    def moveLeft(self):
        self.direction.x = -1

    def moveRight(self):
        self.direction.x = 1


    def update(self):
        self.move()
