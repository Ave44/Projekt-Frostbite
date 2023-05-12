from pygame.sprite import Group
from os import listdir


class SavefileGroups:
    def __init__(self):
        self.createGroupsForModulesInPath('./game/entities')
        self.createGroupsForModulesInPath('./game/objects')
        self.createGroupsForModulesInPath('./game/objects/trees')
        self.createGroupsForModulesInPath('./game/items')

    def createGroupsForModulesInPath(self, path: str):
        for className in listdir(path):
            if className.endswith(".py"):
                setattr(self, className[:-3], Group())

    def createSavefileSpritesData(self) -> dict:
        savefile = {}
        for attribute in vars(self):
            # print(attribute)
            savefile[attribute] = []
            group: Group = getattr(self, attribute)
            for instance in group.sprites():
                instanceData = instance.getSaveData()
                if instanceData:
                    savefile[attribute].append(instanceData)
        return savefile
