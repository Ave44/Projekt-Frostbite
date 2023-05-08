from pygame.image import load
from pygame import Surface
from os import listdir


class LoadedImages:
    def __init__(self):
        self.loadEntitiesImages()
        self.loadAnimatedEntitiesImages()
        self.loadObjectsImages()
        self.loadItemsImages()
        self.loadUiImages()
        self.loadLightsImages()
        self.loadWeatherImages()

    def loadEntitiesImages(self):
        self.player = self.loadEntityImages("./graphics/entities/player", "player")
        self.rabbit = self.loadEntityImages("./graphics/entities/rabbit", "rabbit")
        self.deer = self.loadEntityImages("./graphics/entities/deer", "deer")
        self.boar = self.loadEntityImages("./graphics/entities/boar", "boar")
        self.bomb = self.loadEntityImages("./graphics/entities/bomb", "bomb")
        self.goblin = self.loadEntityImages("./graphics/entities/goblin", "goblin")

    def loadAnimatedEntitiesImages(self):
        self.goblinchampion = self.loadAnimatedEntityImages("./graphics/animated_entities/goblinchampion", "goblinchampion")

    def loadObjectsImages(self):
        self.treeSapling = [load("./graphics/objects/trees/sapling.png").convert_alpha()]
        self.smallTree = [load("./graphics/objects/trees/smallTree.png").convert_alpha()]
        self.mediumTree = [load("./graphics/objects/trees/mediumTree.png").convert_alpha()]
        self.largeTree = [load("./graphics/objects/trees/largeTree.png").convert_alpha()]
        self.snag = [load("./graphics/objects/trees/snag.png").convert_alpha()]
        self.burntTree = load("./graphics/objects/trees/burntTree.png").convert_alpha()

        self.grass = self.loadImages("./graphics/objects/grass", "grass")
        self.grassPicked = load("./graphics/objects/grassPicked.png").convert_alpha()

        self.rock = load("./graphics/objects/rock.png").convert_alpha()

        self.rabbitHole = load("./graphics/objects/rabbit_hole.png").convert_alpha()

        self.goblinHideout = load("./graphics/objects/goblin_hideout.png").convert_alpha()

    def loadItemsImages(self):
        self.undefined = load("./graphics/items/undefined.png").convert_alpha()
        self.bigMeat = load("./graphics/items/big_meat.png").convert_alpha()
        self.boarFang = load("./graphics/items/boar_fang.png").convert_alpha()
        self.goblinFang = load("./graphics/items/goblin_fang.png").convert_alpha()
        self.deerAntlers = load("./graphics/items/deer_antlers.png").convert_alpha()
        self.leather = load("./graphics/items/leather.png").convert_alpha()
        self.smallMeat = load("./graphics/items/small_meat.png").convert_alpha()
        self.sword = load("./graphics/items/sword.png").convert_alpha()
        self.stoneAxe = load("./graphics/items/stoneAxe.png").convert_alpha()
        self.stonePickaxe = load("./graphics/items/stonePickaxe.png").convert_alpha()
        self.woodenArmor = load("./graphics/items/woodenArmor.png").convert_alpha()
        self.leatherArmor = load("./graphics/items/leatherArmor.png").convert_alpha()

        self.pebble = load("./graphics/items/pebble.png").convert_alpha()
        self.grassFibers = load("./graphics/items/grassFibers.png").convert_alpha()
        self.accorn = load("./graphics/items/accorn.png").convert_alpha()
        self.sharpRock = load("./graphics/items/sharpRock.png").convert_alpha()
        self.wood = load("./graphics/items/wood.png").convert_alpha()

    def loadUiImages(self):
        self.slot = load("./graphics/ui/slot.png").convert_alpha()
        self.slotBody = load("./graphics/ui/slotBody.png").convert_alpha()
        self.slotHand = load("./graphics/ui/slotHand.png").convert_alpha()
        self.pointer = load("./graphics/ui/pointer.png").convert_alpha()

    def loadLightsImages(self):
        self.smallLight = load("./graphics/lights/smallLight.png").convert_alpha()
        self.mediumLight = load("./graphics/lights/mediumLight.png").convert_alpha()
        self.largeLight = load("./graphics/lights/largeLight.png").convert_alpha()

    def loadWeatherImages(self):
        self.rain = self.loadImages("./graphics/weathers/rain", "rain_drops")

    def loadImages(self, path: str, filename: str) -> list[Surface]:
        filesAmount = len(listdir(path))
        imagesList = []
        for index in range(filesAmount):
            image = load(f"{path}/{filename}{index + 1}.png").convert_alpha()
            imagesList.append(image)
        return imagesList

    def loadEntityImages(self, path: str, filename: str) -> dict:
        try:
            return {
                "image_up": load(f"{path}/{filename}_up.png").convert_alpha(),
                "image_down": load(f"{path}/{filename}_down.png").convert_alpha(),
                "image_left": load(f"{path}/{filename}_left.png").convert_alpha(),
                "image_right": load(f"{path}/{filename}_right.png").convert_alpha(),

                "image_up_damage": load(f"{path}/{filename}_up_damage.png").convert_alpha(),
                "image_down_damage": load(f"{path}/{filename}_down_damage.png").convert_alpha(),
                "image_left_damage": load(f"{path}/{filename}_left_damage.png").convert_alpha(),
                "image_right_damage": load(f"{path}/{filename}_right_damage.png").convert_alpha(),

                "image_up_heal": load(f"{path}/{filename}_up_heal.png").convert_alpha(),
                "image_down_heal": load(f"{path}/{filename}_down_heal.png").convert_alpha(),
                "image_left_heal": load(f"{path}/{filename}_left_heal.png").convert_alpha(),
                "image_right_heal": load(f"{path}/{filename}_right_heal.png").convert_alpha()
            }
        except Exception:
            print(f"\nMissing images at '{path}/{filename}'\n")
            raise

    def loadAnimatedEntityImages(self, path: str, filename: str) -> dict:
        try:
            return {
                "images_idle": self.loadImages(f"{path}/{filename}_idle", ""),
                "images_up": self.loadImages(f"{path}/{filename}_up", ""),
                "images_down": self.loadImages(f"{path}/{filename}_down", ""),
                "images_left": self.loadImages(f"{path}/{filename}_left", ""),
                "images_right": self.loadImages(f"{path}/{filename}_right", ""),

                "images_idle_damage": self.loadImages(f"{path}/{filename}_idle_damage", ""),
                "images_up_damage": self.loadImages(f"{path}/{filename}_up_damage", ""),
                "images_down_damage": self.loadImages(f"{path}/{filename}_down_damage", ""),
                "images_left_damage": self.loadImages(f"{path}/{filename}_left_damage", ""),
                "images_right_damage": self.loadImages(f"{path}/{filename}_right_damage", ""),

                "images_idle_heal": self.loadImages(f"{path}/{filename}_idle_heal", ""),
                "images_up_heal": self.loadImages(f"{path}/{filename}_up_heal", ""),
                "images_down_heal": self.loadImages(f"{path}/{filename}_down_heal", ""),
                "images_left_heal": self.loadImages(f"{path}/{filename}_left_heal", ""),
                "images_right_heal": self.loadImages(f"{path}/{filename}_right_heal", ""),
            }
        except Exception:
            print(f"\nMissing images at '{path}/{filename}'\n")
            raise
