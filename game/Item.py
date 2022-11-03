import pygame.sprite

class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = None

    def drop(self, param):
        pass

    def use(self):
        pass
