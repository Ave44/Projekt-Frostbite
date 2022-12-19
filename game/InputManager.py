import sys

from pygame.sprite import Sprite
from pygame.math import Vector2

from config import *
from game.entities.Player import Player
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.UiSpriteGroup import UiSpriteGroup


class InputManager:
    def __init__(self, player: Player, UiSprites: UiSpriteGroup, visibleSprites: CameraSpriteGroup):
        self.player = player
        self.UiSprites = UiSprites
        self.visibleSprites = visibleSprites

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

            if event.type == pygame.MOUSEBUTTONUP:
                mouseHoversOverInventory = self.checkIfMouseHoversOverInventory(mousePos)
                hoveredSprite = self.getHoveredSprite(mousePos)

                if event.button == 1:
                    if mouseHoversOverInventory:
                        self.player.inventory.handleMouseLeftClick(mousePos, self.player.selectedItem)
                    elif hoveredSprite:
                        self.player.handleMouseLeftClick(hoveredSprite)
                    elif not self.player.selectedItem.isEmpty():   
                        mousePosInWorld = mousePos + self.visibleSprites.offset
                        self.player.selectedItem.handleMouseLeftClick(mousePosInWorld)
                    else:
                        mousePosInWorld = mousePos + self.visibleSprites.offset
                        self.player.destinationPosition = mousePosInWorld

                if event.button == 3:
                    if mouseHoversOverInventory:
                        self.player.inventory.handleMouseRightClick(mousePos)
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

    def checkIfMouseHoversOverInventory(self, mousePos) -> bool:
        if self.UiSprites.inventory.rect.collidepoint(mousePos):
            return True
        return False

    def getHoveredSprite(self, mousePos) -> Sprite | None:
        mousePosInWorld = mousePos + self.visibleSprites.offset

        for sprite in self.visibleSprites.sprites():
            if sprite.rect.collidepoint(mousePosInWorld):
                return sprite
        return None
