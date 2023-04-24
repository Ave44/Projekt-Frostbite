from pygame.mixer import Sound


class LoadedSounds:
    def __init__(self):
        self.loadEntitiesSounds()
        self.loadObjectsSounds()
        self.loadItemsSounds()

    def loadEntitiesSounds(self):
        self.player = {
            "idle": Sound("./sounds/entities/player/idle.wav"),
            "movement": Sound("./sounds/entities/player/movement.wav"),
            "attack": Sound("./sounds/entities/player/attack.wav"),
            "damaged": Sound("./sounds/entities/player/damaged.wav"),
        }

        self.rabbit = {
            "idle": Sound("./sounds/entities/rabbit/idle.wav"),
            "movement": Sound("./sounds/entities/rabbit/movement.wav"),
            "attack": Sound("./sounds/entities/rabbit/attack.wav"),
            "damaged": Sound("./sounds/entities/rabbit/damaged.wav"),
        }

        self.deer = {
            "idle": Sound("./sounds/entities/deer/idle.wav"),
            "movement": Sound("./sounds/entities/deer/movement.wav"),
            "attack": Sound("./sounds/entities/deer/attack.wav"),
            "damaged": Sound("./sounds/entities/deer/damaged.wav"),
        }

        self.boar = {
            "idle": Sound("./sounds/entities/boar/idle.wav"),
            "movement": Sound("./sounds/entities/boar/movement.wav"),
            "attack": Sound("./sounds/entities/boar/attack.wav"),
            "damaged": Sound("./sounds/entities/boar/damaged.wav"),
        }

        self.bomb = {
            "idle": Sound("./sounds/entities/bomb/idle.wav"),
            "movement": Sound("./sounds/entities/bomb/movement.wav"),
            "attack": Sound("./sounds/entities/bomb/attack.wav"),
            "damaged": Sound("./sounds/entities/bomb/damaged.wav"),
        }

        self.goblin = {
            "idle": Sound("./sounds/entities/goblin/idle.wav"),
            "movement": Sound("./sounds/entities/goblin/movement.wav"),
            "attack": Sound("./sounds/entities/goblin/attack.wav"),
            "damaged": Sound("./sounds/entities/goblin/damaged.wav"),
        }

    def loadObjectsSounds(self):
        self.burning = None

    def loadItemsSounds(self):
        self.meatEat = None

        self.swordSlash = None
        self.shovelDig = None
        self.pickaxeHit = None
