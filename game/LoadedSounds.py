from pygame.mixer import Sound


class LoadedSounds:
    def __init__(self):
        self.loadEntitiesSounds()
        self.loadObjectsSounds()
        self.loadItemsSounds()

    def loadEntitiesSounds(self):
        self.player = {
            "idle": None,
            "movement": None,
            "attack": None,
            "damaged": None,
        }

        self.rabbit = {
            "idle": None,
            "movement": None,
            "attack": None,
            "damaged": None,
        }

        self.deer = {
            "idle": None,
            "movement": None,
            "attack": None,
            "damaged": None,
        }

        self.boar = {
            "idle": None,
            "movement": None,
            "attack": None,
            "damaged": None,
        }

        self.bomb = {
            "idle": None,
            "movement": None,
            "attack": None,
            "damaged": None,
        }

        self.goblin = {
            "idle": Sound("./sounds/entities/goblin/idle.mp3"),
            "movement": Sound("./sounds/entities/goblin/movement.mp3"),
            "attack": Sound("./sounds/entities/goblin/attack.mp3"),
            "damaged": Sound("./sounds/entities/goblin/damaged.mp3"),
        }

    def loadObjectsSounds(self):
        self.burning = None

    def loadItemsSounds(self):
        self.meatEat = None

        self.swordSlash = None
        self.shovelDig = None
        self.pickaxeHit = None
