import pygame

from config import UI_HEALTHBAR_INCREASE, UI_HEALTHBAR_DECREASE, UI_HEALTHBAR_MAIN
from entities.Entity import Entity
from game.ui.inventory.Inventory import Inventory
from ui.Bar import Bar
from items.Item import Item
from ui.inventory.slot.SelectedItem import SelectedItem


class Player(Entity):
    def __init__(self,
                 groups: pygame.sprite.Group,
                 obstacleSprites: pygame.sprite.Group,
                 playerData,
                 inventory: Inventory):
        super().__init__(groups, obstacleSprites, playerData)
        self.selectedItem = SelectedItem(self)
        self.inventory = inventory

        self.healthBar = Bar(pygame.Vector2(115, 50), self.maxHealth, self.currentHealth, 20, 200, UI_HEALTHBAR_MAIN,
                             UI_HEALTHBAR_INCREASE, UI_HEALTHBAR_DECREASE)

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
