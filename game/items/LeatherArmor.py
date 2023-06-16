from pygame import Vector2
from game.LoadedImages import LoadedImages

from game.items.domain.Armor import Armor
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class LeatherArmor(Armor):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages, id: str = None):
        name = "Leather Armor"
        image = loadedImages.leatherArmor
        icon = loadedImages.leatherArmor
        protectionFlat = 0
        gainedDamageModifier = 0.6

        Armor.__init__(self, visibleSprites, center, loadedImages, name, image, icon,
                       protectionFlat, gainedDamageModifier, id)
