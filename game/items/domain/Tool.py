class Tool():
    def __init__(self, damage: int, durability: int, toolPower: float = 1):
        self.toolPower = toolPower
        self.damage = damage
        self.durability = durability
