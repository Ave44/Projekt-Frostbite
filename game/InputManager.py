import pygame
import sys

from game.Player import Player
from game.UiSpriteGroup import UiSpriteGroup
from game.ui.inventory.Inventory import Inventory

class InputManager:
    def __init__(self, player: Player, UiSprites: UiSpriteGroup):
        self.player = player
        self.UiSprites = UiSprites

    def handleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.player.inventory.toggle()


            if event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()
                mouseHoversOverUi = self.checkIfMouseHoversOverUi(mousePos)

                if event.button == 1:
                    if mouseHoversOverUi:
                        self.player.inventory.handleMouseLeftClick(mousePos, self.player.selectedItem)
                    else:
                        pass

                if event.button == 2:
                    if mouseHoversOverUi:
                        self.player.inventory.handleMouseRightClick(mousePos, self.player.selectedItem)
                    else:
                        pass


        pressedKeys = pygame.key.get_pressed()

        if pressedKeys[pygame.K_w]:
            self.player.moveUp()
        elif pressedKeys[pygame.K_s]:
            self.player.moveDown()

        if pressedKeys[pygame.K_a]:
            self.player.moveLeft()
        elif pressedKeys[pygame.K_d]:
            self.player.moveRight()


    def checkIfMouseHoversOverUi(self, mousePos) -> bool:
        if self.UiSprites.inventory.rect.collidepoint(mousePos):
            return True
        return False