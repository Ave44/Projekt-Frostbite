import pygame


class SelectedItem(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()

        self.item = None
        self.player = player

    def isEmpty(self) -> bool:
        return True if self.item is None else False

    def addItem(self, item):
        if self.isEmpty():
            self.item = item
        else:
            self.item.drop(self.player.rect.midbottom)
            self.item = item

    def removeItem(self):
        self.item = None

    def drop(self):
        self.item.drop(self.player.rect.midbottom)
        self.removeItem()

    def action(self, entity):
        self.drop()

    def handleMouseRightClick(self, mousePos):
        self.drop()

    def handleMouseLeftClick(self, mousePosInWorld):
        self.player.setDestination(mousePosInWorld, self)
