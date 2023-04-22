from game.items.domain.Tool import Tool

class Hammer():
    def __init__(self, damage, durability):
        Tool.__init__(self, damage, durability)
