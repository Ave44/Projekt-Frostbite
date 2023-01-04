import pygame

from config import HEALTHBAR_INCREASE, HEALTHBAR_DECREASE, HEALTHBAR_MAIN
from game.entities.Entity import Entity
from game.ui.inventory.Inventory import Inventory
from game.items.Item import Item
from game.ui.inventory.slot.SelectedItem import SelectedItem
from game.ui.Bar import Bar
from pygame.math import Vector2



class Player(Entity):
    def __init__(self,
                 groups: pygame.sprite.Group,
                 obstacleSprites: pygame.sprite.Group,
                 playerData,
                 inventory: Inventory):
        super().__init__(groups, obstacleSprites, playerData)
        self.selectedItem = SelectedItem(self)
        self.inventory = inventory

        self.healthBar = Bar(Vector2(115, 50), self.maxHealth, self.currentHealth, 20, 200, HEALTHBAR_MAIN,
                             HEALTHBAR_INCREASE, HEALTHBAR_DECREASE)

    def stopAutowalking(self):
        self.destinationPosition = None
        self.destinationTarget = None

    def moveUp(self):
        self.direction.y = -1
        self.stopAutowalking()

    def moveDown(self):
        self.direction.y = 1
        self.stopAutowalking()

    def moveLeft(self):
        self.direction.x = -1
        self.stopAutowalking()

    def moveRight(self):
        self.direction.x = 1
        self.stopAutowalking()

    def handleMouseLeftClick(self, sprite):
        if isinstance(sprite, Item):
            self.setDestination(Vector2(sprite.rect.center), sprite)
            # self.inventory.addItem(sprite, self.selectedItem)

    def update(self):
        self.move()
        self.healthBar.update(self.currentHealth)

    def die(self):
        self.healthBar.update(self.currentHealth)
        # self.remove(*self.groups())
        print("Game Over")
