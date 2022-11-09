import pygame
from config import WINDOW_HEIGHT, WINDOW_WIDTH
from game.ui.inventory.Slot import Slot


class CameraSpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.halfWindowHeight = WINDOW_HEIGHT // 2
        self.halfWindowWidth = WINDOW_WIDTH // 2
        self.offset = pygame.math.Vector2()

    def customDraw(self, center):
        self.displaySurface.fill('black')
        self.offset.x = center.x - self.halfWindowWidth
        self.offset.y = center.y - self.halfWindowHeight

        for sprite in self.sprites():
            spritePosition = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, spritePosition)
            if type(sprite) == Slot and not sprite.isEmpty():
                self.displaySurface.blit(sprite.item.icon, spritePosition)
