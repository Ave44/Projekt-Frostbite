from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup

from pygame import Rect
from pygame.sprite import Group, Sprite
from pygame.time import Clock
from pygame.math import Vector2

from math import ceil
from constants import HEALTHBAR_MAIN, HEALTHBAR_INCREASE, HEALTHBAR_DECREASE, HUNGERBAR_MAIN, HUNGERBAR_INCREASE, HUNGERBAR_DECREASE, SLOT_GAP
from Config import Config
from game.LoadedImages import LoadedImages
from game.LoadedSounds import LoadedSounds
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup
from game.entities.domain.Entity import Entity
from game.lightning.Glowing import Glowing
from game.ui.inventory.Inventory import Inventory
from game.ui.inventory.slot.Slot import Slot
from game.items.domain.Tool import Tool
from game.items.domain.Armor import Armor
from game.ui.inventory.slot.SelectedItem import SelectedItem
from game.ui.Bar import Bar
from game.LoadedImages import LoadedImages


class Player(Entity, Glowing):
    def __init__(self,
                 visibleSprites: CameraSpriteGroup,
                 obstacleSprites: Group,
                 UiSprites: UiSpriteGroup,
                 loadedImages: LoadedImages,
                 loadedSounds: LoadedSounds,
                 config: Config,
                 clock: Clock,
                 midbottom: Vector2,
                 currHealth: int = None,
                 currHunger: float = None):
        playerData = {"speed": 6, "maxHealth": 100, "maxHunger": 100, "actionRange": 20, "hungerDecreasePerMS": 0.0001}
        self.maxHunger = playerData["maxHunger"]
        self.hungerDecreasePerMS = playerData["hungerDecreasePerMS"]
        self.currHunger = currHunger if currHunger else self.maxHunger
        self.handDamage = 3

        colliderRect = Rect((0, 0), (20, 20))
        self.visibleSprites = visibleSprites
        Entity.__init__(self, visibleSprites, obstacleSprites, playerData, loadedImages.player, loadedSounds.player, colliderRect, clock, midbottom, currHealth)

        playerSize = self.rect.size
        offset = Vector2(-100, -100) + Vector2(playerSize[0] // 2, playerSize[1] // 2)
        Glowing.__init__(self, loadedImages.mediumLight, self.rect, offset)

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

        self.healthBar = Bar(Vector2(115, 50), self.maxHealth, self.currHealth, 20, 200,
                             HEALTHBAR_MAIN, HEALTHBAR_INCREASE, HEALTHBAR_DECREASE)
        self.hungerBar = Bar(Vector2(115, 90), self.maxHunger, self.currHunger, 20, 200,
                             HUNGERBAR_MAIN, (255,0,0),(255,0,0))#HUNGERBAR_INCREASE, HUNGERBAR_DECREASE)

    def moveInDirection(self):
        Entity.moveInDirection(self)
        self.direction.xy = [0, 0]

    def adjustRect(self):
        self.rect.midbottom = self.colliderRect.midbottom
        if not self.destinationPosition:
            self.direction.xy = [0, 0]

    def stopAutowalking(self):
        self.destinationPosition = None
        self.midDestinationPosition = None
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
        self.setDestination(Vector2(sprite.rect.midbottom), sprite)

    def drop(self) -> None:
        pass

    def damage(self):
        if self.handSlot.item:
            return self.handSlot.item.damage
        return self.handDamage

    def getDamage(self, amount: int) -> None:
        if self.bodySlot.item:
            amount = self.bodySlot.item.reduceDamage(amount)
        Entity.getDamage(self, amount)

    def die(self, deathMessage: str = "Game Over"):
        self.currHealth = 0
        self.healthBar.update(self.currHealth)
        self.remove(*self.groups())
        self.drop()
        print(deathMessage)

    def updateHunger(self):
        deltaTime = self.clock.get_time()
        self.currHunger -= self.hungerDecreasePerMS * deltaTime
        if self.currHunger <= 0:
            self.currHunger = 0
            self.getDamage(1, 'hunger')

    def satiate(self, numberOfHungerToSatiate: int):
        if self.currHunger + numberOfHungerToSatiate < self.maxHunger:
            self.currHunger = self.currHunger + numberOfHungerToSatiate
        else:
            self.currHunger = self.maxHunger

    def subtractHunger(self, value: int):
        if self.currHunger - value > 0:
            self.currHunger -= value
        else:
            self.currHunger = 0

    def localUpdate(self):
        self.updateHunger()
        # print("{:3.4f}".format(self.currHunger), ceil(self.currHunger))
        self.hungerBar.update(100)#ceil(self.currHunger))
        self.healthBar.update(self.currHealth)
        self.move()

    def getSaveData(self) -> dict:
        inventoryData = {'inventory': self.inventory.getSaveData(), 'handSlot': self.handSlot.getItemId(), 'bodySlot': self.bodySlot.getItemId()}
        return {'midbottom': self.rect.midbottom, 'currHealth': self.currHealth, 'currHunger': self.currHunger, 'inventoryData': inventoryData}

    def populateEquipment(self, inventoryData: dict) -> None:
        inventorySaveData = inventoryData['inventory']['slotsItemData']
        for itemIdIndex in range(len(inventorySaveData)):
            itemId = inventorySaveData[itemIdIndex]
            if itemId != None:
                item = self.visibleSprites.getItemById(itemId)
                item.hide()
                self.inventory.slotList[itemIdIndex].addItem(item)

        if inventoryData['handSlot'] != None:
            item = self.visibleSprites.getItemById(inventoryData['handSlot'])
            item.hide()
            self.handSlot.addItem(item)

        if inventoryData['bodySlot'] != None:
            item = self.visibleSprites.getItemById(inventoryData['bodySlot'])
            item.hide()
            self.bodySlot.addItem(item)
        self.hungerBar.update(self.currHunger)
        self.move()
