import pygame

from game.Entity import Entity
from game.items.Item import Item
from game.ui.SelectedItem import SelectedItem
from game.ui.inventory.Inventory import Inventory


class Player(Entity):
    def __init__(self, 
                groups: list[pygame.sprite.Group],
                obstacleSprites: pygame.sprite.Group,
                playerData,
                inventory: Inventory):

        super().__init__(groups, obstacleSprites, playerData)
        self.selectedItem = SelectedItem(self)
        self.inventory = inventory


    def moveUp(self):
        self.direction.y = -1

    def moveDown(self):
        self.direction.y = 1

    def moveLeft(self):
        self.direction.x = -1

    def moveRight(self):
        self.direction.x = 1

    def handleMouseLeftClick(self, sprite):
        if isinstance(sprite, Item):
            self.inventory.addItem(sprite, self.selectedItem)

    def update(self):
        self.move()
