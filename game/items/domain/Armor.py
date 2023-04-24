from abc import ABC


class Armor(ABC):
    def __init__(self, protectionFlat: int = 0, gainedDamageModifier: float = 1):
        self.protectionFlat = protectionFlat
        self.gainedDamageModifier = gainedDamageModifier

    def reduceDamage(self, amount: int):
        reducedAmount = int((amount - self.protectionFlat) * self.gainedDamageModifier)
        return reducedAmount
