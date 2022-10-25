import pygame
from config import WINDOW_HEIGTH, WINDOW_WIDTH

class CameraSpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.halfWindowHeight = WINDOW_HEIGTH // 2
        self.halfWindowWidth = WINDOW_WIDTH // 2
        self.offset = pygame.math.Vector2()

    def customDraw(self, center):
        self.displaySurface.fill('black')
        self.offset.x = center.x - self.halfWindowWidth
        self.offset.y = center.y - self.halfWindowHeight

        for sprite in self.sprites():
            spritePosition = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, spritePosition)