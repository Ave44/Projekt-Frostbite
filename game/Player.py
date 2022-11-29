import pygame
from pygame.math import Vector2

from game.Entity import Entity
from game.items.Item import Item
from game.ui.Bar import Bar
from game.ui.SelectedItem import SelectedItem
from game.ui.inventory.Inventory import Inventory


class Player(Entity):
    def __init__(self,
                 groups: list[pygame.sprite.Group],
                 obstacleSprites: pygame.sprite.Group,
                 playerData,
                 inventory: Inventory,
                 maxHealth: int):
        super().__init__(groups, obstacleSprites, playerData, maxHealth, maxHealth)
        self.selectedItem = SelectedItem(self)
        self.inventory = inventory
        self.healthBar = Bar(Vector2(10, 40), self.maxHealth, self.currentHealth, 20, 200, 'red', 'green', 'yellow')

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
        self.healthBar.update(self.currentHealth)

    def die(self):
        self.healthBar.update(self.currentHealth)
        self.remove(*self.groups())
        print("Game Over")
