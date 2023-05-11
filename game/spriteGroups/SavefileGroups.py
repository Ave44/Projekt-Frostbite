from pygame.sprite import Group
from os import listdir
from json import dump


class SavefileGroups:
    def __init__(self):
        for className in listdir('./game/entities'):
            if className.endswith(".py"):
                setattr(self, className[:-3], Group())

        for className in listdir('./game/objects'):
            if className.endswith(".py"):
                setattr(self, className[:-3], Group())

        for className in listdir('./game/objects/trees'):
            if className.endswith(".py"):
                setattr(self, className[:-3], Group())

        for className in listdir('./game/items'):
            if className.endswith(".py"):
                setattr(self, className[:-3], Group())

    def createSavefileData(self) -> dict:
        savefile = {}
        for attribute in vars(self):
            savefile[attribute] = []
            group: Group = getattr(self, attribute)
            for instance in group.sprites():
                savefile[attribute].append(instance.getSaveData())
        return savefile

    def saveGame(self, filename: str):
        savefileData = self.createSavefileData()
        with open(f"savefiles/{filename}.json", "w") as file:
            dump(savefileData, file)
