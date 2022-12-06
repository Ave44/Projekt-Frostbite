import pygame

from entities.Entity import Entity
from ui.inventory.items.Item import Item
from ui.inventory.state.SelectedItem import SelectedItem
from game.ui.inventory.Inventory import Inventory


class Player(Entity):
    def __init__(self,
                 groups: pygame.sprite.Group,
                 obstacleSprites: pygame.sprite.Group,
                 playerData,
                 inventory: Inventory):
        super().__init__(groups, obstacleSprites, playerData)
        self.selectedItem = SelectedItem(self)
        self.inventory = inventory

    def move_up(self):
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
