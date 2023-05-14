from pygame import Vector2
from game.LoadedImages import LoadedImages

from game.items.domain.Armor import Armor
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class WoodenArmor(Armor):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages, id: str = None):
        name = "WoodenArmor"
        image = loadedImages.woodenArmor
        icon = loadedImages.woodenArmor
        protectionFlat = 0
        gainedDamageModifier = 0.5

        Armor.__init__(self, visibleSprites, center, loadedImages, name, image, icon,
                       protectionFlat, gainedDamageModifier, id)
