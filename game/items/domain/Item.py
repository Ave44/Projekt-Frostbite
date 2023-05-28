from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.entities.Player import Player
    from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
import shortuuid

from pygame import Surface
from pygame.sprite import Sprite
from pygame.math import Vector2

from game.LoadedImages import LoadedImages


class Item(Sprite):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages,
                 name: str = "Unknown", image: Surface = None, icon: Surface = None, id: str = None):
        Sprite.__init__(self, visibleSprites)
        self.visibleSprites = visibleSprites
        self.visibleSprites.items.add(self)
        savefileGroup = getattr(visibleSprites.savefileGroups, type(self).__name__)
        savefileGroup.add(self)
        self.id = id if id else shortuuid.uuid()

        self.name = name
        self.image = image
        if not image:
            self.image = loadedImages.undefined

        self.icon = icon
        if not icon:
            self.icon = loadedImages.undefined

        self.rect = self.image.get_rect(center=center)

    def drop(self, position: Vector2) -> None:
        self.rect.midbottom = position
        self.show()

    def onLeftClickAction(self, player: Player):
        player.inventory.addItem(self, player.selectedItem)

    def show(self):
        self.add(self.visibleSprites)

    def hide(self):
        self.remove(self.visibleSprites)

    def getSaveData(self) -> dict:
        return {'center': self.rect.center, 'id': self.id}
    
    def setSaveData(self, savefileData: dict):
        self.rect.center = savefileData['center']
        self.id = savefileData['id']