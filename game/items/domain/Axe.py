from pygame import Surface

from game.items.domain.Tool import Tool


class Axe(Tool):
    def __init__(self, visibleSprites, center, loadedImages, damage, durability,
                 name: str = None, image: Surface = None, icon: Surface = None,
                 id: str = None, currDurability: int = None, toolPower: float = 1):
        Tool.__init__(self, visibleSprites, center, loadedImages, damage, durability, name, image, icon, id, currDurability, toolPower)
