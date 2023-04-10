import pygame


class LoadedSounds:
    def __init__(self):
        self.loadEntitiesSounds()
        self.loadObjectsSounds()
        self.loadItemsSounds()

    def loadEntitiesSounds(self):
        self.player = {
            "idle": pygame.mixer.Sound("./sounds/entities/player/idle.wav"),
            "movement": pygame.mixer.Sound("./sounds/entities/player/movement.wav"),
            "attack": pygame.mixer.Sound("./sounds/entities/player/attack.wav"),
            "damaged": pygame.mixer.Sound("./sounds/entities/player/damaged.wav"),
        }

        self.rabbit = {
            "idle": pygame.mixer.Sound("./sounds/entities/rabbit/idle.wav"),
            "movement": pygame.mixer.Sound("./sounds/entities/rabbit/movement.wav"),
            "attack": pygame.mixer.Sound("./sounds/entities/rabbit/attack.wav"),
            "damaged": pygame.mixer.Sound("./sounds/entities/rabbit/damaged.wav"),
        }

        self.deer = {
            "idle": pygame.mixer.Sound("./sounds/entities/deer/idle.wav"),
            "movement": pygame.mixer.Sound("./sounds/entities/deer/movement.wav"),
            "attack": pygame.mixer.Sound("./sounds/entities/deer/attack.wav"),
            "damaged": pygame.mixer.Sound("./sounds/entities/deer/damaged.wav"),
        }

        self.boar = {
            "idle": pygame.mixer.Sound("./sounds/entities/boar/idle.wav"),
            "movement": pygame.mixer.Sound("./sounds/entities/boar/movement.wav"),
            "attack": pygame.mixer.Sound("./sounds/entities/boar/attack.wav"),
            "damaged": pygame.mixer.Sound("./sounds/entities/boar/damaged.wav"),
        }

        self.bomb = {
            "idle": pygame.mixer.Sound("./sounds/entities/bomb/idle.wav"),
            "movement": pygame.mixer.Sound("./sounds/entities/bomb/movement.wav"),
            "attack": pygame.mixer.Sound("./sounds/entities/bomb/attack.wav"),
            "damaged": pygame.mixer.Sound("./sounds/entities/bomb/damaged.wav"),
        }

        self.goblin = {
            "idle": pygame.mixer.Sound("./sounds/entities/goblin/idle.wav"),
            "movement": pygame.mixer.Sound("./sounds/entities/goblin/movement.wav"),
            "attack": pygame.mixer.Sound("./sounds/entities/goblin/attack.wav"),
            "damaged": pygame.mixer.Sound("./sounds/entities/goblin/damaged.wav"),
        }

    def loadObjectsSounds(self):
        self.burning = None

    def loadItemsSounds(self):
        self.meatEat = None

        self.swordSlash = None
        self.shovelDig = None
        self.pickaxeHit = None
