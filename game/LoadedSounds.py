from pygame.mixer import Sound


class LoadedSounds:
    def __init__(self):
        self.loadEntitiesSounds()
        self.loadObjectsSounds()
        self.loadItemsSounds()

    def loadEntitiesSounds(self):
        self.player = {
            "idle": Sound("./sounds/entities/player/idle.mp3"),
            "movement": Sound("./sounds/entities/player/movement.mp3"),
            "attack": Sound("./sounds/entities/player/attack.mp3"),
            "damaged": Sound("./sounds/entities/player/damaged.mp3"),
        }

        self.rabbit = {
            "idle": Sound("./sounds/entities/rabbit/idle.mp3"),
            "movement": Sound("./sounds/entities/rabbit/movement.mp3"),
            "attack": Sound("./sounds/entities/rabbit/attack.mp3"),
            "damaged": Sound("./sounds/entities/rabbit/damaged.mp3"),
        }

        self.deer = {
            "idle": Sound("./sounds/entities/deer/idle.mp3"),
            "movement": Sound("./sounds/entities/deer/movement.mp3"),
            "attack": Sound("./sounds/entities/deer/attack.mp3"),
            "damaged": Sound("./sounds/entities/deer/damaged.mp3"),
        }

        self.boar = {
            "idle": Sound("./sounds/entities/boar/idle.mp3"),
            "movement": Sound("./sounds/entities/boar/movement.mp3"),
            "attack": Sound("./sounds/entities/boar/attack.mp3"),
            "damaged": Sound("./sounds/entities/boar/damaged.mp3"),
        }

        self.bomb = {
            "idle": Sound("./sounds/entities/bomb/idle.mp3"),
            "movement": Sound("./sounds/entities/bomb/movement.mp3"),
            "attack": Sound("./sounds/entities/bomb/attack.mp3"),
            "damaged": Sound("./sounds/entities/bomb/damaged.mp3"),
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
