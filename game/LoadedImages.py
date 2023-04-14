from pygame.image import load
from pygame import Surface
from os import listdir

class LoadedImages:
    def __init__(self):
        self.loadEntitiesImages()
        self.loadObjectsImages()
        self.loadItemsImages()
        self.loadLightsImages()
        
    def loadEntitiesImages(self):
        self.player = {
            "image_up": load("./graphics/entities/player/player_up.png").convert_alpha(),
            "image_down": load("./graphics/entities/player/player_down.png").convert_alpha(),
            "image_left": load("./graphics/entities/player/player_left.png").convert_alpha(),
            "image_right": load("./graphics/entities/player/player_right.png").convert_alpha(),

            "image_up_damage": load("./graphics/entities/player/player_up_damage.png").convert_alpha(),
            "image_down_damage": load("./graphics/entities/player/player_down_damage.png").convert_alpha(),
            "image_left_damage": load("./graphics/entities/player/player_left_damage.png").convert_alpha(),
            "image_right_damage": load("./graphics/entities/player/player_right_damage.png").convert_alpha(),

            "image_up_heal": load("./graphics/entities/player/player_up_heal.png").convert_alpha(),
            "image_down_heal": load("./graphics/entities/player/player_down_heal.png").convert_alpha(),
            "image_left_heal": load("./graphics/entities/player/player_left_heal.png").convert_alpha(),
            "image_right_heal": load("./graphics/entities/player/player_right_heal.png").convert_alpha()
        }

        self.rabbit = {
            "image_up": load("./graphics/entities/rabbit/rabbit_up.png").convert_alpha(),
            "image_down": load("./graphics/entities/rabbit/rabbit_down.png").convert_alpha(),
            "image_left": load("./graphics/entities/rabbit/rabbit_left.png").convert_alpha(),
            "image_right": load("./graphics/entities/rabbit/rabbit_right.png").convert_alpha(),

            "image_up_damage": load("./graphics/entities/rabbit/rabbit_up_damage.png").convert_alpha(),
            "image_down_damage": load("./graphics/entities/rabbit/rabbit_down_damage.png").convert_alpha(),
            "image_left_damage": load("./graphics/entities/rabbit/rabbit_left_damage.png").convert_alpha(),
            "image_right_damage": load("./graphics/entities/rabbit/rabbit_right_damage.png").convert_alpha(),

            "image_up_heal": load("./graphics/entities/rabbit/rabbit_up_heal.png").convert_alpha(),
            "image_down_heal": load("./graphics/entities/rabbit/rabbit_down_heal.png").convert_alpha(),
            "image_left_heal": load("./graphics/entities/rabbit/rabbit_left_heal.png").convert_alpha(),
            "image_right_heal": load("./graphics/entities/rabbit/rabbit_right_heal.png").convert_alpha()
        }

        self.deer = {
            "image_up": load("./graphics/entities/deer/deer_up.png").convert_alpha(),
            "image_down": load("./graphics/entities/deer/deer_down.png").convert_alpha(),
            "image_left": load("./graphics/entities/deer/deer_left.png").convert_alpha(),
            "image_right": load("./graphics/entities/deer/deer_right.png").convert_alpha(),

            "image_up_damage": load("./graphics/entities/deer/deer_up_damage.png").convert_alpha(),
            "image_down_damage": load("./graphics/entities/deer/deer_down_damage.png").convert_alpha(),
            "image_left_damage": load("./graphics/entities/deer/deer_left_damage.png").convert_alpha(),
            "image_right_damage": load("./graphics/entities/deer/deer_right_damage.png").convert_alpha(),

            "image_up_heal": load("./graphics/entities/deer/deer_up_heal.png").convert_alpha(),
            "image_down_heal": load("./graphics/entities/deer/deer_down_heal.png").convert_alpha(),
            "image_left_heal": load("./graphics/entities/deer/deer_left_heal.png").convert_alpha(),
            "image_right_heal": load("./graphics/entities/deer/deer_right_heal.png").convert_alpha()
        }

        self.boar = {
            "image_up": load("./graphics/entities/boar/boar_up.png").convert_alpha(),
            "image_down": load("./graphics/entities/boar/boar_down.png").convert_alpha(),
            "image_left": load("./graphics/entities/boar/boar_left.png").convert_alpha(),
            "image_right": load("./graphics/entities/boar/boar_right.png").convert_alpha(),

            "image_up_heal": load("./graphics/entities/boar/boar_up_heal.png").convert_alpha(),
            "image_down_heal": load("./graphics/entities/boar/boar_down_heal.png").convert_alpha(),
            "image_left_heal": load("./graphics/entities/boar/boar_left_heal.png").convert_alpha(),
            "image_right_heal": load("./graphics/entities/boar/boar_right_heal.png").convert_alpha(),

            "image_up_damage": load("./graphics/entities/boar/boar_up_damage.png").convert_alpha(),
            "image_down_damage": load("./graphics/entities/boar/boar_down_damage.png").convert_alpha(),
            "image_left_damage": load("./graphics/entities/boar/boar_left_damage.png").convert_alpha(),
            "image_right_damage": load("./graphics/entities/boar/boar_right_damage.png").convert_alpha()
        }

        self.bomb = {
            "image_up": load("./graphics/entities/enemy/enemy.png").convert_alpha(),
            "image_down": load("./graphics/entities/enemy/enemy.png").convert_alpha(),
            "image_left": load("./graphics/entities/enemy/enemy.png").convert_alpha(),
            "image_right": load("./graphics/entities/enemy/enemy.png").convert_alpha(),

            "image_up_heal": load("./graphics/entities/enemy/enemy.png").convert_alpha(),
            "image_down_heal": load("./graphics/entities/enemy/enemy.png").convert_alpha(),
            "image_left_heal": load("./graphics/entities/enemy/enemy.png").convert_alpha(),
            "image_right_heal": load("./graphics/entities/enemy/enemy.png").convert_alpha(),

            "image_up_damage": load("./graphics/entities/enemy/enemy.png").convert_alpha(),
            "image_down_damage": load("./graphics/entities/enemy/enemy.png").convert_alpha(),
            "image_left_damage": load("./graphics/entities/enemy/enemy.png").convert_alpha(),
            "image_right_damage": load("./graphics/entities/enemy/enemy.png").convert_alpha()
        }

        self.goblin = {
            "image_up": load("./graphics/entities/goblin/goblin_up.png").convert_alpha(),
            "image_down": load("./graphics/entities/goblin/goblin_down.png").convert_alpha(),
            "image_left": load("./graphics/entities/goblin/goblin_left.png").convert_alpha(),
            "image_right": load("./graphics/entities/goblin/goblin_right.png").convert_alpha(),

            "image_up_heal": load("./graphics/entities/goblin/goblin_up_heal.png").convert_alpha(),
            "image_down_heal": load("./graphics/entities/goblin/goblin_down_heal.png").convert_alpha(),
            "image_left_heal": load("./graphics/entities/goblin/goblin_left_heal.png").convert_alpha(),
            "image_right_heal": load("./graphics/entities/goblin/goblin_right_heal.png").convert_alpha(),

            "image_up_damage": load("./graphics/entities/goblin/goblin_up_damage.png").convert_alpha(),
            "image_down_damage": load("./graphics/entities/goblin/goblin_down_damage.png").convert_alpha(),
            "image_left_damage": load("./graphics/entities/goblin/goblin_left_damage.png").convert_alpha(),
            "image_right_damage": load("./graphics/entities/goblin/goblin_right_damage.png").convert_alpha()
        }


    def loadObjectsImages(self):
        self.treeSapling = [load("./graphics/objects/trees/sapling.png").convert_alpha()]
        self.smallTree = [load("./graphics/objects/trees/smallTree.png").convert_alpha()]
        self.mediumTree = [load("./graphics/objects/trees/mediumTree.png").convert_alpha()]
        self.largeTree = [load("./graphics/objects/trees/largeTree.png").convert_alpha()]
        self.snag = [load("./graphics/objects/trees/snag.png").convert_alpha()]
        self.burntTree = load("./graphics/objects/trees/burntTree.png").convert_alpha()

        self.grass = self.loadImages("./graphics/objects/grass", "grass")

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

        self.pebble = load("./graphics/items/pebble.png").convert_alpha()
        self.grassFibers = load("./graphics/items/grassFibers.png").convert_alpha()
        # self.accorn = load("./graphics/items/accorn.png").convert_alpha()
        self.sharpRock = load("./graphics/items/sharpRock.png").convert_alpha()
        self.wood = load("./graphics/items/wood.png").convert_alpha()

    def loadLightsImages(self):
        self.smallLight = load("./graphics/lights/smallLight.png").convert_alpha()
        self.mediumLight = load("./graphics/lights/mediumLight.png").convert_alpha()
        self.largeLight = load("./graphics/lights/largeLight.png").convert_alpha()

    def loadImages(self, path: str, filename) -> list[Surface]:
        filesAmount = len(listdir(path))
        imagesList = []
        for index in range(filesAmount):
            image = load(f"{path}/{filename}{index + 1}.png").convert_alpha()
            imagesList.append(image)
        return imagesList
