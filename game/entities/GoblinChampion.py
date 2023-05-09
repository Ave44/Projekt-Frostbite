from pygame import Vector2, Rect
from pygame.time import Clock

from game.LoadedImages import LoadedImages
from game.LoadedSounds import LoadedSounds
from game.entities.domain.AggressiveMob import AggressiveMob
from game.items.BigMeat import BigMeat
from game.items.GoblinFang import GoblinFang
from game.spriteGroups.CameraSpriteGroup import CameraSpriteGroup
from game.spriteGroups.ObstacleSprites import ObstacleSprites
from game.entities.domain.Entity import Entity
from game.entities.domain.AnimatedEntity import AnimatedEntity
from game.objects.domain.Object import Object
from game.entities.Goblin import Goblin


class GoblinChampion(AnimatedEntity, Goblin):
    def __init__(self, visibleSprites: CameraSpriteGroup, obstacleSprites: ObstacleSprites,
                 loadedImages: LoadedImages, loadedSounds: LoadedSounds, clock: Clock, midbottom: Vector2,
                 currHealth: int = None):
        entityData = {
            "speed": 1,
            "maxHealth": 100,
            "damage": 20,
            "sightRange": 150,
            "actionRange": 50,
            "moveEveryMs": 700,
            "minMoveTimeMs": 500,
            "maxMoveTimeMs": 1000,
            "attackCooldownMs": 2000
        }
        colliderRect = Rect((0, 0), (10, 10))
        AggressiveMob.__init__(self, visibleSprites, obstacleSprites, loadedImages.goblin, loadedSounds.goblin, colliderRect, entityData, clock, midbottom, currHealth)
        AnimatedEntity.__init__(self, visibleSprites, loadedImages.goblinchampion, clock)

        self.loadedImages = loadedImages

    def attack(self, target: Entity | Object):
        AggressiveMob.attack(self, target)
        self.playSound(self.soundAttack)

    def drop(self) -> None:
        BigMeat(self.visibleSprites, self.rect.center, self.loadedImages)
        GoblinFang(self.visibleSprites, self.rect.center, self.loadedImages)
