import sys

import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2

from game.entities.Player import Player
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup
from game.ui.inventory.slot.Slot import Slot
from game.ui.crafting.Recipe import Recipe


class InputManager:
    def __init__(self, player: Player, UiSprites: UiSpriteGroup, visibleSprites: CameraSpriteGroup, saveGame: callable, goBackToMenu: callable):
        self.player = player
        self.UiSprites = UiSprites
        self.visibleSprites = visibleSprites
        self.saveGame = saveGame
        self.goBackToMenu = goBackToMenu
        pygame.event.clear()

    def handleInput(self) -> None:
        mousePos = Vector2(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.player.inventory.toggle()

                if event.key == pygame.K_o:
                    self.player.getDamage(20)

                if event.key == pygame.K_p:
                    self.player.heal(20)

                if event.key == pygame.K_h:
                    self.visibleSprites.toggleShowHitboxes()

                if event.key == pygame.K_l:
                    self.saveGame()

                if event.key == pygame.K_ESCAPE:
                    self.goBackToMenu()

            if event.type == pygame.MOUSEBUTTONUP:
                mouseHoversOverInventory = self.checkIfMouseHoversOverInventory(mousePos)
                mouseHoversOverCrafting = self.checkIfMouseHoversOverCrafting(mousePos)
                hoveredSprite = self.getHoveredSprite(mousePos)

                if event.button == 1:
                    if mouseHoversOverInventory:
                        hoveredSlot = self.getHoveredSlotSprite(mousePos)
                        if hoveredSlot:
                            hoveredSlot.handleMouseLeftClick(self.player)
                    elif mouseHoversOverCrafting:
                        hoveredRecipe = self.getHoveredRecipe(mousePos)
                        if hoveredRecipe:
                            hoveredRecipe.craft(self.player.inventory, self.player.selectedItem)
                    elif hoveredSprite:
                        if not isinstance(hoveredSprite, Player):
                            self.player.handleMouseLeftClick(hoveredSprite)
                    elif not self.player.selectedItem.isEmpty():
                        mousePosInWorld = mousePos + self.visibleSprites.offset
                        self.player.selectedItem.handleMouseLeftClick(mousePosInWorld)
                    else:
                        mousePosInWorld = mousePos + self.visibleSprites.offset
                        self.player.setDestination(mousePosInWorld)

                if event.button == 3:
                    if mouseHoversOverInventory:
                        hoveredSlot = self.getHoveredSlotSprite(mousePos)
                        if hoveredSlot:
                            hoveredSlot.handleMouseRightClick(self.player)
                    elif not self.player.selectedItem.isEmpty():
                        self.player.selectedItem.handleMouseRightClick(mousePos)

        pressedKeys = pygame.key.get_pressed()

        if pressedKeys[pygame.K_w]:
            self.player.moveUp()
        elif pressedKeys[pygame.K_s]:
            self.player.moveDown()

        if pressedKeys[pygame.K_a]:
            self.player.moveLeft()
        elif pressedKeys[pygame.K_d]:
            self.player.moveRight()

    def checkIfMouseHoversOverInventory(self, mousePos: Vector2) -> bool:
        return self.UiSprites.inventory.rect.collidepoint(mousePos) or self.UiSprites.equipmentBackgroundRect.collidepoint(mousePos)

    def checkIfMouseHoversOverCrafting(self, mousePos: Vector2) -> bool:
        return self.UiSprites.crafting.rect.collidepoint(mousePos)

    def getHoveredSprite(self, mousePos: Vector2) -> Sprite:
        mousePosInWorld = mousePos + self.visibleSprites.offset

        for sprite in self.visibleSprites.sprites():
            if sprite.rect.collidepoint(mousePosInWorld):
                spriteMask = pygame.mask.from_surface(sprite.image)
                mousePositionAtMaskX = mousePosInWorld.x - sprite.rect.x
                mousePositionAtMaskY = mousePosInWorld.y - sprite.rect.y
                mousePositionAtMask = (mousePositionAtMaskX, mousePositionAtMaskY)
                if spriteMask.get_at(mousePositionAtMask):
                    return sprite
        return None

    def getHoveredSlotSprite(self, mousePos) -> Slot:
        if self.player.handSlot.rect.collidepoint(mousePos):
            return self.player.handSlot
        elif self.player.bodySlot.rect.collidepoint(mousePos):
            return self.player.bodySlot
        else:
            hoveredSlot = next(filter(lambda slot: (slot.rect.collidepoint(mousePos)), self.player.inventory.slotList), None)
            return hoveredSlot

    def getHoveredRecipe(self, mousePos) -> Recipe:
        hoveredRecipe = next(filter(lambda recipe: (recipe.rect.collidepoint(mousePos)), self.UiSprites.crafting.recipesList), None)
        return hoveredRecipe
