import pygame
from pygame.math import Vector2

from config import UI_HEALTHBAR_MAIN, UI_HEALTHBAR_INCREASE, UI_HEALTHBAR_DECREASE
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
                 inventory: Inventory):
        super().__init__(groups, obstacleSprites, playerData)
        self.selectedItem = SelectedItem(self)
        self.inventory = inventory
        self.healthBar = Bar(Vector2(115, 50), self.maxHealth, self.currentHealth, 20, 200, UI_HEALTHBAR_MAIN, UI_HEALTHBAR_INCREASE, UI_HEALTHBAR_DECREASE)

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
        # self.remove(*self.groups())
        print("Game Over")
