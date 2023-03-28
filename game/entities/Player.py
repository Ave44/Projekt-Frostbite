import pygame
from pygame.time import Clock

from config import HEALTHBAR_INCREASE, HEALTHBAR_DECREASE, HEALTHBAR_MAIN, WINDOW_WIDTH, WINDOW_HEIGHT
from game.entities.domain.Entity import Entity
from game.ui.inventory.Inventory import Inventory
from game.items.domain.Item import Item
from game.ui.inventory.slot.SelectedItem import SelectedItem
from game.ui.Bar import Bar
from pygame.math import Vector2


class Player(Entity):
    def __init__(self,
                 groups: pygame.sprite.Group,
                 obstacleSprites: pygame.sprite.Group,
                 UiSprites: pygame.sprite.Group,
                 playerImages: dict,
                 clock: Clock,
                 midbottom: Vector2,
                 currHealth: int = None):
        playerData = {"speed": 6, "maxHealth": 100}
        Entity.__init__(self, groups, obstacleSprites, playerData, playerImages, clock, midbottom, currHealth)
        self.selectedItem = SelectedItem(self)

        inventoryPosition = Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 60)
        self.inventory = Inventory(UiSprites, 2, 12, inventoryPosition)
        self.inventory.open()

        UiSprites.player = self
        UiSprites.inventory = self.inventory
        UiSprites.selectedItem = self.selectedItem

        self.healthBar = Bar(Vector2(115, 50), self.maxHealth, self.currentHealth, 20, 200,
                             HEALTHBAR_MAIN, HEALTHBAR_INCREASE, HEALTHBAR_DECREASE)

    def adjustDirection(self):
        if self.destinationPosition:
            self.moveTowards()
        else:
            self.direction.xy = [0, 0]

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

    def drop(self) -> None:
        pass

    def die(self):
        self.currentHealth = 0
        self.healthBar.update(self.currentHealth)
        self.remove(*self.groups())
        self.drop()
        print("Game Over")

    def localUpdate(self):
        self.move()
        self.healthBar.update(self.currentHealth)
