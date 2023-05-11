from pygame import Vector2
from pygame.surface import Surface

from game.items.domain.Item import Item
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.LoadedImages import LoadedImages


class Armor(Item):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages,
                 name: str = None, image: Surface = None, icon: Surface = None, 
                 protectionFlat: int = 0, gainedDamageModifier: float = 1):
        Item.__init__(self, visibleSprites, center, loadedImages, name, image, icon)
        self.protectionFlat = protectionFlat
        self.gainedDamageModifier = gainedDamageModifier

    def reduceDamage(self, amount: int):
        reducedAmount = int((amount - self.protectionFlat) * self.gainedDamageModifier)
        return reducedAmount
