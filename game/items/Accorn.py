from pygame import Vector2
from game.LoadedImages import LoadedImages

from game.entities.Player import Player
from game.items.domain.Item import Item
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup


class Accorn(Item):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages, id: str = None):
        name = "Accorn"
        img = loadedImages.accorn
        icon = loadedImages.accorn
        Item.__init__(self, visibleSprites, center, loadedImages, name, img, icon, id)
        self.hoverMessage = f"Eat {self.name}"

    def use(self, player: Player):
        player.heal(5)
        player.satiate(5)