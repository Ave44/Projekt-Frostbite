from game.items.domain.Tool import Tool

class Axe(Tool):
    def __init__(self, damage, durability):
        Tool.__init__(self, damage, durability)
