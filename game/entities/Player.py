from pygame.sprite import Group, Sprite
from pygame.time import Clock
from pygame.math import Vector2

from constants import HEALTHBAR_MAIN, HEALTHBAR_INCREASE, HEALTHBAR_DECREASE, SLOT_GAP
from Config import Config
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup
from game.entities.domain.Entity import Entity
from game.ui.inventory.Inventory import Inventory
from game.ui.inventory.slot.Slot import Slot
from game.items.domain.Item import Item
from game.items.domain.Tool import Tool
from game.items.domain.Armor import Armor
from game.ui.inventory.slot.SelectedItem import SelectedItem
from game.ui.Bar import Bar
from game.LoadedImages import LoadedImages


class Player(Entity):
    def __init__(self,
                 groups: Group,
                 obstacleSprites: Group,
                 UiSprites: UiSpriteGroup,
                 loadedImages: LoadedImages,
                 config: Config,
                 clock: Clock,
                 midbottom: Vector2,
                 currHealth: int = None):
        playerData = {"speed": 6, "maxHealth": 100}
        Entity.__init__(self, groups, obstacleSprites, playerData, loadedImages.player, clock, midbottom, currHealth)
        self.selectedItem = SelectedItem(self)

        inventoryPosition = Vector2(config.WINDOW_WIDTH / 2, config.WINDOW_HEIGHT - 60)
        self.inventory = Inventory(UiSprites, 2, 12, inventoryPosition, loadedImages)
        self.inventory.open()

        handSlotPosition = self.inventory.rect.topright + Vector2(SLOT_GAP * 2, SLOT_GAP)
        self.handSlot = Slot(handSlotPosition, loadedImages.slotHand, type=Tool)

        bodySlotPosition = self.handSlot.rect.bottomleft + Vector2(0, SLOT_GAP)
        self.bodySlot = Slot(bodySlotPosition, loadedImages.slotBody, type=Armor)

        UiSprites.player = self
        UiSprites.inventory = self.inventory
        UiSprites.selectedItem = self.selectedItem
        UiSprites.setEquipmentSlots(self.handSlot, self.bodySlot)

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

    def handleMouseLeftClick(self, sprite: Sprite):
        # if isinstance(sprite, Item):
            self.setDestination(Vector2(sprite.rect.midbottom), sprite)
            # self.inventory.addItem(sprite, self.selectedItem)

    def drop(self) -> None:
        pass

    def getDamage(self, amount: int) -> None:
        if self.bodySlot.item:
            amount = self.bodySlot.item.reduceDamage(amount)
        Entity.getDamage(self, amount)
        
    def die(self):
        self.currentHealth = 0
        self.healthBar.update(self.currentHealth)
        self.remove(*self.groups())
        self.drop()
        print("Game Over")

    def localUpdate(self):
        self.move()
        self.healthBar.update(self.currentHealth)
