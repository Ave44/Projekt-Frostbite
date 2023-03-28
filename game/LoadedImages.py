from pygame.image import load

class LoadedImages:
    def __init__(self):
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

        self.sapling = [load("./graphics/objects/trees/sapling.png").convert_alpha()]
        self.smallTree = [load("./graphics/objects/trees/smallTree.png").convert_alpha()]
        self.mediumTree = [load("./graphics/objects/trees/mediumTree.png").convert_alpha()]
        self.largeTree = [load("./graphics/objects/trees/largeTree.png").convert_alpha()]
        self.snag = [load("./graphics/objects/trees/snag.png").convert_alpha()]
        self.burntTree = [load("./graphics/objects/trees/burntTree.png").convert_alpha()]

        self.grass = [load("./graphics/objects/grass.png").convert_alpha()]

        self.rock = load("./graphics/objects/rock.png").convert_alpha()

        self.rabbitHole = load("./graphics/objects/rabbit_hole.png").convert_alpha()