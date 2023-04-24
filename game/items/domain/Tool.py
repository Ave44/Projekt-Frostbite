from abc import ABC

class Tool(ABC):
    def __init__(self, damage: int, durability: int, toolPower: float = 1):
        self.toolPower = toolPower
        self.damage = damage
        self.durability = durability

    def reduceDurability(self):
        self.durability -= 1