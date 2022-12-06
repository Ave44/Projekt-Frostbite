import sys

from pygame.sprite import Sprite

from config import *
from entities.Player import Player
from spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from spriteGroups.UiSpriteGroup import UiSpriteGroup


class InputManager:
    def __init__(self, player: Player, UiSprites: UiSpriteGroup, visibleSprites: CameraSpriteGroup):
        self.player = player
        self.UiSprites = UiSprites
        self.visibleSprites = visibleSprites

    def handleInput(self) -> None:
        mousePos = pygame.math.Vector2(pygame.mouse.get_pos())

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

                if event.button == 1:
                    if mouseHoversOverInventory:
                        self.player.inventory.handleMouseLeftClick(mousePos, self.player.selectedItem)
                    elif not self.player.selectedItem.isEmpty():
                        self.player.selectedItem.handleMouseLeftClick(mousePos)
                    else:
                        hoveredSprite = self.getHoveredSprite(mousePos)
                        if hoveredSprite:
                            self.player.handleMouseLeftClick(hoveredSprite)

                if event.button == 3:
                    if mouseHoversOverInventory:
                        self.player.inventory.handleMouseRightClick(mousePos)
                    elif not self.player.selectedItem.isEmpty():
                        self.player.selectedItem.handleMouseRightClick(mousePos)

        pressedKeys = pygame.key.get_pressed()

        if pressedKeys[pygame.K_w]:
            self.player.move_up()
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
