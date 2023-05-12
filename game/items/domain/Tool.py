from pygame import Vector2
from pygame.surface import Surface

from game.items.domain.Item import Item
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.LoadedImages import LoadedImages



class Tool(Item):
    def __init__(self, visibleSprites: CameraSpriteGroup, center: Vector2, loadedImages: LoadedImages,
                 damage: int, maxDurability: int, name: str = None, image: Surface = None,
                 icon: Surface = None, currDurability: int = None, toolPower: float = 1):
        Item.__init__(self, visibleSprites, center, loadedImages, name, image, icon)
        self.toolPower = toolPower
        self.damage = damage
        self.maxDurability = maxDurability
        self.currDurability = currDurability if currDurability else maxDurability

    def reduceDurability(self):
        self.currDurability -= 1

    def getSaveData(self) -> dict:
        return {'center': self.rect.center, 'id': self.id, 'currDurability': self.currDurability}
    
    def setSaveData(self, savefileData: dict):
        self.rect.center = savefileData['center']
        self.id = savefileData['id']
        self.currDurability = savefileData['currDurability']
